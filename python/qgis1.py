# 将下面的 WKT 字符串替换成你从 ASF 复制出来的那串内容
wkt_string = "POLYGON((44.7889 -18.9229,44.8663 -18.9229,44.8663 -18.864,44.7889 -18.864,44.7889 -18.9229))"

# 1. 创建一个临时的多边形图层 (内存图层)，设置坐标系为 WGS84 (EPSG:4326)
layer = QgsVectorLayer("Polygon?crs=epsg:4326", "ASF_BoundingBox", "memory")
pr = layer.dataProvider()

# 2. 从 WKT 字符串生成几何图形
geom = QgsGeometry.fromWkt(wkt_string)
feat = QgsFeature()
feat.setGeometry(geom)

# 3. 将画好的图形加入图层
pr.addFeatures([feat])
layer.updateExtents()

# 4. 将图层加载到 QGIS 的地图画布中
QgsProject.instance().addMapLayer(layer)
print("选框已成功导入！")