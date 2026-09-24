from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY, QgsProject, QgsField
from qgis.gui import QgsMapToolExtent
from qgis.utils import iface
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QFileDialog
from qgis.core import Qgis
import processing
import os
import re
from datetime import datetime

# ================= 1. 坐标解析与点位生成模块 =================

# 预置了之前询问的喀斯特地貌坐标
wiki_inputs = [
    {"name": "荔波喀斯特_小七孔", "coord": "25°00′00″N 104°55′00″E"}
    
]

def parse_wiki_dms(dms_str):
    """解析维基百科格式的度分秒并转为十进制"""
    numbers = re.findall(r"\d+\.?\d*", dms_str)
    if not numbers:
        return 0.0
    d = float(numbers[0])
    m = float(numbers[1]) if len(numbers) > 1 else 0
    s = float(numbers[2]) if len(numbers) > 2 else 0
    dd = d + m/60 + s/3600
    if any(char in dms_str.upper() for char in ['S', 'W']):
        dd = -dd
    return dd

def add_wiki_points():
    """生成坐标点并添加到地图"""
    layer = QgsVectorLayer("Point?crs=EPSG:4326", "喀斯特地貌点位", "memory")
    provider = layer.dataProvider()
    provider.addAttributes([QgsField("Name", QVariant.String), QgsField("Raw_Coord", QVariant.String)])
    layer.updateFields()

    features = []
    for item in wiki_inputs:
        parts = item["coord"].split()
        if len(parts) < 2: continue
        lat_val = parse_wiki_dms(parts[0]) 
        lon_val = parse_wiki_dms(parts[1]) 
        
        fet = QgsFeature()
        fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(lon_val, lat_val)))
        fet.setAttributes([item["name"], item["coord"]])
        features.append(fet)

    provider.addFeatures(features)
    QgsProject.instance().addMapLayer(layer)
    print("-> 步骤1：解析完成！兴趣点已生成。")

# ================= 2. 底图加载模块 =================

def load_base_raster():
    """选择并加载栅格底图"""
    default_dir = r"D:/File/Utility File/哥白尼30米全国县级" 
    if not os.path.exists(default_dir):
        default_dir = ""

    file_path, _ = QFileDialog.getOpenFileName(
        None, "选择要加载的栅格底图 (如 DEM)", default_dir, "Raster Files (*.tif *.png *.dem);;All Files (*)"
    )

    if file_path:
        layer_name = os.path.basename(file_path)
        layer = iface.addRasterLayer(file_path, layer_name)

        if layer and layer.isValid():
            print(f"-> 步骤2：底图 '{layer_name}' 已成功加载。")
            # 缩放到图层范围并将其设为活动图层（重要，裁剪工具需要基于活动图层）
            iface.mapCanvas().setExtent(layer.extent())
            iface.mapCanvas().refresh()
            iface.setActiveLayer(layer) 
            return layer
        else:
            print("错误：无法加载图层。")
    else:
        print("未选择底图。")
    return None

# ================= 3. 鼠标框选裁剪模块 =================

class QuickClipAndSaveTool(QgsMapToolExtent):
    def __init__(self, canvas, save_dir):
        super().__init__(canvas)
        self.canvas = canvas
        self.save_dir = save_dir
        self.target_size = 1024 

    def extentInstantiated(self, extent):
        # 1. 检查图层
        layer = self.canvas.currentLayer()
        if not layer or layer.type() != layer.RasterLayer:
            # 【弹窗警告】没有选中正确的图层
            iface.messageBar().pushMessage("操作无效", "请先在左侧【图层面板】点击高亮你要裁剪的原始 DEM 图层！", level=Qgis.Warning, duration=5)
            return
            
        # 2. 自动修正正方形范围
        width = extent.xMaximum() - extent.xMinimum()
        height = extent.yMaximum() - extent.yMinimum()
        center_x = extent.xMinimum() + width / 2.0
        center_y = extent.yMinimum() + height / 2.0
        side_length = max(width, height)
        
        new_xmin = center_x - side_length / 2.0
        new_xmax = center_x + side_length / 2.0
        new_ymin = center_y - side_length / 2.0
        new_ymax = center_y + side_length / 2.0
        ext_str = f"{new_xmin},{new_xmax},{new_ymin},{new_ymax}"
            
        timestamp = datetime.now().strftime("%H%M%S")
        out_name = f"clipped_karst_{self.target_size}_{timestamp}.tif"
        out_path = os.path.join(self.save_dir, out_name)
        
        params = {
            'INPUT': layer, 
            'PROJWIN': ext_str, 
            'NODATA': None, 
            'OPTIONS': '', 
            'DATA_TYPE': 0, 
            'EXTRA': f'-outsize {self.target_size} {self.target_size}', 
            'OUTPUT': out_path
        }
        
        # 【弹窗提示】开始处理
        iface.messageBar().pushMessage("处理中", "正在裁剪并重采样，请稍候...", level=Qgis.Info, duration=2)
        
        try:
            processing.run("gdal:cliprasterbyextent", params)
            iface.addRasterLayer(out_path, out_name)
            iface.setActiveLayer(layer)
            
            # 【弹窗提示】处理成功
            iface.messageBar().pushMessage("裁剪成功", f"文件已保存至: {out_name}", level=Qgis.Success, duration=3)
        except Exception as e:
            # 【弹窗警告】处理报错
            iface.messageBar().pushMessage("系统错误", f"裁剪失败，请查看Python控制台获取详情。错误信息: {str(e)}", level=Qgis.Critical, duration=10)
            print(f"详细错误日志: {e}")

def activate_clip_tool():
    """激活鼠标框选裁剪工具"""
    default_save_dir = r"D:/File/Research/dataset/DanXia/png"
    if not os.path.exists(default_save_dir):
        default_save_dir = ""
        
    save_dir = QFileDialog.getExistingDirectory(None, "请选择裁剪出来的影像保存的文件夹", default_save_dir)
    
    if save_dir:
        canvas = iface.mapCanvas()
        global custom_clip_tool 
        custom_clip_tool = QuickClipAndSaveTool(canvas, save_dir)
        canvas.setMapTool(custom_clip_tool)
        
        # 激活成功提示
        iface.messageBar().pushMessage("工具已就绪", "请在地图上拖拽框选。记得先在左侧选中要裁剪的底图！", level=Qgis.Success, duration=5)

# ================= 4. 主控执行逻辑 =================
def run_workflow():
    print("=== 开始综合工作流 ===")
    add_wiki_points()
    
    # 稍微暂停提示一下
    base_layer = load_base_raster()
    
    if base_layer:
        activate_clip_tool()
    else:
        print("工作流提前结束。")

# 执行主流程
run_workflow()