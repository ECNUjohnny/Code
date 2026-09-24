from qgis.core import (QgsCoordinateReferenceSystem, QgsCoordinateTransform, 
                       QgsProject, QgsPointXY, Qgis)
from qgis.utils import iface
from PyQt5.QtWidgets import QFileDialog, QInputDialog
import processing
import os
import re
import random
from datetime import datetime

def parse_coordinate_input(coord_input):
    """智能解析：同时支持度分秒与十进制，支持空格或逗号分隔"""
    import re
    # 将常见的逗号（包含中英文）替换为空格，方便统一拆分
    clean_input = coord_input.replace(',', ' ').replace('，', ' ')
    # 过滤掉多余空格，提取出纬度和经度两部分
    parts = [p for p in clean_input.split() if p.strip()]
    
    if len(parts) < 2:
        return None, None
        
    def parse_single(val_str):
        # 提取这部分中的所有数字
        numbers = re.findall(r"-?\d+\.?\d*", val_str)
        if not numbers:
            return 0.0
        
        # 核心逻辑：如果只有一个数字，说明是纯十进制 (如 "25.123" 或 "25.123N")
        if len(numbers) == 1:
            dd = float(numbers[0])
        else:
            # 包含多个数字，说明是度分秒格式 (如 "25°30′15″")
            d = float(numbers[0])
            m = float(numbers[1])
            s = float(numbers[2]) if len(numbers) > 2 else 0
            dd = d + m/60.0 + s/3600.0
            
        # 自动识别南纬(S)和西经(W)的负数逻辑
        if any(char in val_str.upper() for char in ['S', 'W']) and dd > 0:
            dd = -dd
        return dd

    # 默认第一个值是纬度，第二个值是经度
    lat_val = parse_single(parts[0])
    lon_val = parse_single(parts[1])
    return lat_val, lon_val

def parse_wiki_dms(dms_str):
    """解析度分秒或十进制字符串为浮点数"""
    numbers = re.findall(r"-?\d+\.?\d*", dms_str)
    if not numbers:
        return 0.0
    d = float(numbers[0])
    m = float(numbers[1]) if len(numbers) > 1 else 0
    s = float(numbers[2]) if len(numbers) > 2 else 0
    dd = d + m/60 + s/3600
    if any(char in dms_str.upper() for char in ['S', 'W']):
        dd = -dd
    return dd

def generate_random_crops_from_coord():
    # 1. 检查是否选中了栅格图层
    layer = iface.activeLayer()
    if not layer or layer.type() != layer.RasterLayer:
        iface.messageBar().pushMessage("错误", "请先在左侧面板点击选中你的底图（栅格图层）", level=Qgis.Warning, duration=5)
        return

    # 2. 接收用户输入坐标 (可以输入度分秒，也可以直接输十进制，空格隔开)
    # 示例输入: 25°00′00″N 104°55′00″E 或者 25.0 104.91
    coord_input, ok1 = QInputDialog.getText(None, "输入坐标", "请输入经纬度坐标 (纬度 经度，用空格隔开):", text="25°00′00″N 104°55′00″E")
    if not ok1 or not coord_input:
        return

    # 3. 接收生成数量
    num_samples, ok2 = QInputDialog.getInt(None, "生成数量", "你想在这个点周围随机生成多少张图片？", value=5, min=1, max=100)
    if not ok2:
        return

    # 4. 选择保存文件夹 (默认指向你的数据集路径)
    default_dir = r"D:/File/Research/dataset/Kasite"
    if not os.path.exists(default_dir):
        default_dir = ""
    save_dir = QFileDialog.getExistingDirectory(None, "选择保存数据集的文件夹", default_dir)
    if not save_dir:
        return

    # ------------------ 核心测算逻辑 ------------------
    # 解析输入的经纬度
    # === 新的智能调用代码 ===
    lat_val, lon_val = parse_coordinate_input(coord_input)
    if lat_val is None:
        iface.messageBar().pushMessage("输入错误", "无法识别坐标，请确保输入了纬度和经度两个值。", level=Qgis.Critical, duration=5)
        return

    # 将输入的 EPSG:4326(经纬度) 转换为当前栅格底图的投影坐标系
    crs_src = QgsCoordinateReferenceSystem("EPSG:4326")
    crs_dest = layer.crs()
    transform = QgsCoordinateTransform(crs_src, crs_dest, QgsProject.instance())
    
    try:
        pt_lonlat = QgsPointXY(lon_val, lat_val)
        pt_layer = transform.transform(pt_lonlat) # 转换后的中心点 (地图单位，通常是米)
    except Exception as e:
        iface.messageBar().pushMessage("转换错误", "坐标转换失败，请检查输入的坐标格式。", level=Qgis.Critical, duration=5)
        return

    # 获取底图的像素分辨率 (表示1个像素代表现实中多少地图单位)
    pixel_width = layer.rasterUnitsPerPixelX()
    pixel_height = layer.rasterUnitsPerPixelY()
    
    # 计算 256x256 像素在地图上对应的实际宽度和高度
    target_size = 256
    box_width = pixel_width * target_size
    box_height = pixel_height * target_size

    # 设定随机抖动的范围 (例如：中心点最多偏移半个框的距离)
    max_shift_x = box_width / 2.5
    max_shift_y = box_height / 2.5

    iface.messageBar().pushMessage("开始生成", f"正在围绕目标点生成 {num_samples} 张 256x256 切片...", level=Qgis.Info, duration=3)

    # ------------------ 循环随机裁剪 ------------------
    success_count = 0
    for i in range(num_samples):
        # 随机产生平移量
        shift_x = random.uniform(-max_shift_x, max_shift_x)
        shift_y = random.uniform(-max_shift_y, max_shift_y)
        
        # 计算新框的中心点
        new_center_x = pt_layer.x() + shift_x
        new_center_y = pt_layer.y() + shift_y
        
        # 计算框的四个角
        xmin = new_center_x - box_width / 2.0
        xmax = new_center_x + box_width / 2.0
        ymin = new_center_y - box_height / 2.0
        ymax = new_center_y + box_height / 2.0
        
        ext_str = f"{xmin},{xmax},{ymin},{ymax}"
        out_name = f"aug_crop_{target_size}_{datetime.now().strftime('%H%M%S')}_{i+1}.tif"
        out_path = os.path.join(save_dir, out_name)
        
        # 使用 -outsize 强制保证输出由于浮点数计算误差可能导致的像素多1少1的问题
        params = {
            'INPUT': layer,
            'PROJWIN': ext_str,
            'NODATA': None,
            'OPTIONS': '',
            'DATA_TYPE': 0,
            'EXTRA': f'-outsize {target_size} {target_size}',
            'OUTPUT': out_path
        }
        
        try:
            processing.run("gdal:cliprasterbyextent", params)
            success_count += 1
            print(f"[{i+1}/{num_samples}] 已生成: {out_name}")
        except Exception as e:
            print(f"[{i+1}/{num_samples}] 生成失败: {e}")

    iface.messageBar().pushMessage("完成", f"成功生成 {success_count} 张图像！", level=Qgis.Success, duration=5)

# 执行脚本
generate_random_crops_from_coord()