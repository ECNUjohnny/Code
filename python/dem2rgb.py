import os
import rasterio
import requests
import numpy as np
from PIL import Image
import io
import time

# ================= 1. 路径配置 =================
# 你刚才用滑动窗口切出来的小尺寸 DEM 文件夹
DEM_DIR = "./ML_Dataset_Augmented_Full" 
# 用于存放对应卫星图的新文件夹
RGB_DIR = "./ML_Dataset_RGB_Paired"      
os.makedirs(RGB_DIR, exist_ok=True)

# ArcGIS 免费无认证高清卫星图接口
ESRI_URL = "https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/export"

# 获取所有切好的小高程图
dem_files = [f for f in os.listdir(DEM_DIR) if f.endswith('.tif')]
print(f"准备为 {len(dem_files)} 个 DEM 样本下载完全对齐的卫星图...\n")

# ================= 2. 执行对齐抓取 =================
for i, filename in enumerate(dem_files):
    dem_path = os.path.join(DEM_DIR, filename)
    rgb_path = os.path.join(RGB_DIR, filename) # 卫星图使用相同的文件名，方便 ML 训练时按名字匹配
    
    # 如果已经下载过了，支持断点续传
    if os.path.exists(rgb_path):
        continue
        
    try:
        # 步骤 1：读取 DEM 的极其精确的地理边界
        with rasterio.open(dem_path) as src:
            bounds = src.bounds # 获取 (左, 下, 右, 上) 的真实地理坐标
            width = src.width
            height = src.height
            
            # 复制 DEM 的元数据（这是保持地理空间一致性的灵魂）
            meta = src.meta.copy()

        # 步骤 2：构造向卫星图服务器请求的参数
        bbox_str = f"{bounds.left},{bounds.bottom},{bounds.right},{bounds.top}"
        params = {
            "bbox": bbox_str,
            "bboxSR": "4326",    # 声明边界坐标系为 WGS84 经纬度
            "imageSR": "4326",   # 请求返回的图像坐标系也为 WGS84
            "size": f"{width},{height}", # 强制要求返回 256x256 像素
            "format": "png",     # 获取无损的 PNG 图片流
            "f": "image"         # 直接返回图像而不是 JSON
        }
        
        # 步骤 3：下载高清卫星图
        response = requests.get(ESRI_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            # 步骤 4：将普通的 PNG 图片转换为科学的 GeoTIFF 格式
            # 使用 PIL 将二进制流读取为 RGB 图像
            img = Image.open(io.BytesIO(response.content)).convert("RGB")
            img_array = np.array(img) # 形状此时是 (256, 256, 3)
            
            # Rasterio 要求的格式是 (波段数, 高, 宽)，所以需要把颜色通道移到最前面
            img_array = np.transpose(img_array, (2, 0, 1)) 
            
            # 步骤 5：更新元数据，从单通道高程图改为 3 通道彩色图
            meta.update({
                "count": 3,              # R, G, B 三个通道
                "dtype": "uint8",        # 颜色值是 0-255 的整数
                "nodata": None           # 卫星图通常不需要特殊的无数据掩码
            })
            
            # 步骤 6：写入本地
            with rasterio.open(rgb_path, "w", **meta) as dest:
                dest.write(img_array)
                
            print(f"[{i+1}/{len(dem_files)}] 卫星图配对成功: {filename}")
            
        else:
            print(f"[{i+1}/{len(dem_files)}] 下载失败: 状态码 {response.status_code}")
            
    except Exception as e:
        print(f"[{i+1}/{len(dem_files)}] 发生异常: {filename} - {e}")
        
    # 稍微停顿一下，避免并发请求过多被 Esri 临时屏蔽
    time.sleep(0.5)

print("\n🎉 全部配对完成！你现在拥有了一套极高价值的【RGB卫星图-高程DEM】多模态训练集！")