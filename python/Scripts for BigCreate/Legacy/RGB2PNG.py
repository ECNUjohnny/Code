import os
import rasterio
import numpy as np
from PIL import Image

# 输入和输出路径
INPUT_DIR = "D:\File\Research\dataset\RGB from CDSE"
VISUAL_DIR = "D:\File\Research\dataset\RGB_Visual"
os.makedirs(VISUAL_DIR, exist_ok=True)

def stretch_image(data):
    """2% 累积直方图拉伸算法"""
    # 过滤掉 0 (通常是黑边/无数据区)
    valid_data = data[data > 0]
    if valid_data.size == 0:
        return np.zeros_like(data, dtype=np.uint8)
        
    # 计算 2% 和 98% 的百分位数作为拉伸边界
    p2, p98 = np.percentile(valid_data, (2, 98))
    
    # 执行拉伸：将 [p2, p98] 映射到 [0, 255]
    stretched = np.clip((data - p2) * 255.0 / (p98 - p2), 0, 255)
    return stretched.astype(np.uint8)

tif_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.tif')]

for filename in tif_files:
    in_path = os.path.join(INPUT_DIR, filename)
    out_path = os.path.join(VISUAL_DIR, filename.replace('.tif', '.jpg'))
    
    print(f"正在美化预览图: {filename}...")
    
    with rasterio.open(in_path) as src:
        # 读取红(B1)、绿(B2)、蓝(B3)三个波段
        r = src.read(1)
        g = src.read(2)
        b = src.read(3)
        
        # 分别对每个波段进行直方图拉伸
        r_s = stretch_image(r)
        g_s = stretch_image(g)
        b_s = stretch_image(b)
        
        # 合并为 RGB 三通道彩色图
        rgb_composite = np.dstack((r_s, g_s, b_s))
        
        # 保存为常规 JPG
        img = Image.fromarray(rgb_composite)
        img.save(out_path, quality=95)

print("\n🎉 所有卫星图已完成‘补光’！快去 RGB_Visual 文件夹看看大峡谷的真容吧。")