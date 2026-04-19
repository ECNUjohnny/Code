from qgis.core import (QgsCoordinateReferenceSystem, QgsCoordinateTransform, 
                       QgsProject, QgsPointXY, Qgis)
from qgis.utils import iface
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox
import processing
import os
import re
import random
from datetime import datetime

def parse_coords(text):
    """解析单个坐标文本"""
    clean = text.replace(',', ' ').replace('，', ' ')
    parts = [p for p in clean.split() if p.strip()]
    if len(parts) < 2: return None, None
    
    def get_num(val):
        nums = re.findall(r"-?\d+\.?\d*", val)
        if not nums: return 0.0
        if len(nums) == 1: dd = float(nums[0])
        else: dd = float(nums[0]) + float(nums[1])/60.0 + (float(nums[2]) if len(nums)>2 else 0)/3600.0
        if any(char in val.upper() for char in ['S', 'W']) and dd > 0: dd = -dd
        return dd
        
    return get_num(parts[0]), get_num(parts[1])

def run_tool():
    layer = iface.activeLayer()
    if not layer or layer.type() != layer.RasterLayer:
        iface.messageBar().pushMessage("错误", "请先选中底图", level=Qgis.Warning, duration=5)
        return

    # 提取图层名并清理特殊字符，支持中文
    raw_name = layer.name()
    safe_name = re.sub(r'[\\/*?:"<>|]', '', raw_name).replace(' ', '_')

    reply = QMessageBox.question(None, "选择模式", "是否要划定一个范围【自动撒网】生成坐标？\n\n选 Yes：输入边界框自动生成坐标\n选 No：手动粘贴具体的坐标列表", QMessageBox.Yes | QMessageBox.No)
    
    pts = [] 
    
    if reply == QMessageBox.Yes:
        bbox, ok = QInputDialog.getText(None, "输入范围", "请输入: 最小纬度, 最大纬度, 最小经度, 最大经度\n(用逗号隔开):", text="24.96, 25.02, 104.90, 104.96")
        if not ok or not bbox: return
        try:
            b = [float(x.strip()) for x in bbox.split(',')]
            min_lat, max_lat, min_lon, max_lon = b[0], b[1], b[2], b[3]
        except:
            iface.messageBar().pushMessage("错误", "范围格式填写错误", level=Qgis.Warning, duration=3)
            return
            
        n_pts, ok = QInputDialog.getInt(None, "点位数量", "你想在这个范围生成多少个坐标点？", value=80, min=1)
        if not ok: return
        
        for _ in range(n_pts):
            pts.append((random.uniform(min_lat, max_lat), random.uniform(min_lon, max_lon)))
            
    else:
        txt, ok = QInputDialog.getMultiLineText(None, "粘贴坐标", "请粘贴经纬坐标（每行一个点）：")
        if not ok or not txt.strip(): return
        
        for line in txt.strip().split('\n'):
            if not line.strip(): continue
            lat, lon = parse_coords(line)
            if lat is not None: pts.append((lat, lon))

    if not pts: return

    n_imgs, ok = QInputDialog.getInt(None, "切片数量", f"共获得 {len(pts)} 个坐标。\n\n每个坐标点附近随机切多少张图？", value=3, min=1)
    if not ok: return

    out_dir = QFileDialog.getExistingDirectory(None, "选择保存文件夹", r"D:/File/Research/dataset/DanXia/png")
    if not out_dir: return

    crs_src = QgsCoordinateReferenceSystem("EPSG:4326")
    trans = QgsCoordinateTransform(crs_src, layer.crs(), QgsProject.instance())
    px_w, px_h = layer.rasterUnitsPerPixelX(), layer.rasterUnitsPerPixelY()
    size = 256
    box_w, box_h = px_w * size, px_h * size

    print(f"=== 开始处理图层: {raw_name} ===")
    done = 0
    total = len(pts) * n_imgs
    
    for pt_idx, (lat, lon) in enumerate(pts):
        try:
            pt_map = trans.transform(QgsPointXY(lon, lat))
            for i in range(n_imgs):
                dx, dy = random.uniform(-box_w/2, box_w/2), random.uniform(-box_h/2, box_h/2)
                nx, ny = pt_map.x() + dx, pt_map.y() + dy
                
                ext = f"{nx - box_w/2},{nx + box_w/2},{ny - box_h/2},{ny + box_h/2}"
                
                time_str = datetime.now().strftime('%H%M%S')
                fname = f"{safe_name}_pt{pt_idx+1}_{i+1}_{time_str}.tif"
                path = os.path.join(out_dir, fname)
                
                # 直接输出原生的 TIF 文件
                params = {'INPUT': layer, 'PROJWIN': ext, 'EXTRA': f'-outsize {size} {size}', 'OUTPUT': path}
                processing.run("gdal:cliprasterbyextent", params)
                
                done += 1
                print(f"[{done}/{total}] {fname} 已生成")
        except: 
            continue

    QMessageBox.information(None, "完成", f"图层处理完毕！\n成功生成 {done} 张 TIF 图片。")

run_tool()