from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY, QgsProject, QgsField
from PyQt5.QtCore import QVariant
import re

# 1. 在这里直接粘贴从 Wiki 复制的坐标字符串
wiki_inputs = [
    {"name": "乐昌乐安鼻", "coord": "25°12′29″N 105°02′36″E"},
    
]

def parse_wiki_dms(dms_str):
    """解析维基百科格式的度分秒并转为十进制"""
    # 提取所有数字（包括小数）
    numbers = re.findall(r"\d+\.?\d*", dms_str)
    if not numbers:
        return 0.0
    
    # 按照 度, 分, 秒 的顺序读取
    d = float(numbers[0])
    m = float(numbers[1]) if len(numbers) > 1 else 0
    s = float(numbers[2]) if len(numbers) > 2 else 0
    
    # 计算十进制
    dd = d + m/60 + s/3600
    
    # 判断方位：如果是南纬(S)或西经(W)，则为负数
    if any(char in dms_str.upper() for char in ['S', 'W']):
        dd = -dd
    return dd

# 2. 创建内存图层
layer = QgsVectorLayer("Point?crs=EPSG:4326", "Wiki_Locations", "memory")
provider = layer.dataProvider()
provider.addAttributes([QgsField("Name", QVariant.String), QgsField("Raw_Coord", QVariant.String)])
layer.updateFields()

# 3. 解析并添加点
features = []
for item in wiki_inputs:
    # 维基百科格式通常是 Latitude(N/S)在前, Longitude(E/W)在后
    # 我们用正则或空格拆分这两个部分
    parts = item["coord"].split()
    if len(parts) < 2: continue
    
    lat_val = parse_wiki_dms(parts[0]) # 纬度 Y
    lon_val = parse_wiki_dms(parts[1]) # 经度 X
    
    fet = QgsFeature()
    fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(lon_val, lat_val)))
    fet.setAttributes([item["name"], item["coord"]])
    features.append(fet)

provider.addFeatures(features)

# 4. 加载到项目
QgsProject.instance().addMapLayer(layer)
print("解析完成！点已生成。")