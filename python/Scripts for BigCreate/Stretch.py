import os
from PIL import Image

# ==========================================
# 1. 基础配置
# ==========================================
# 你要处理的区域名称（需与之前下载的文件夹名一致）
REGION_NAME = "Mount_Everest_Peak"

# 目标分辨率 (宽, 高)
# 方案A：统一缩小到 512x512（推荐深度学习使用，省硬盘）
# 方案B：统一放大到 1068x1068（保留最高清晰度，但 DEM 会插值放大）
TARGET_SIZE = (512, 512) 

# ==========================================
# 2. 路径设置
# ==========================================
# 原始数据文件夹
raw_dem_dir = f"./dataset/{REGION_NAME}/DEM"
raw_s2_dir = f"./dataset/{REGION_NAME}/S2"

# 经过对齐处理后的新文件夹 (加了 _Aligned 后缀)
out_dem_dir = f"./dataset/{REGION_NAME}_Aligned/DEM"
out_s2_dir = f"./dataset/{REGION_NAME}_Aligned/S2"

# 自动创建输出文件夹
os.makedirs(out_dem_dir, exist_ok=True)
os.makedirs(out_s2_dir, exist_ok=True)

# ==========================================
# 3. 批量处理与对齐
# ==========================================
print(f"🚀 开始处理区域: {REGION_NAME}")
print(f"📏 目标统一分辨率: {TARGET_SIZE[0]} x {TARGET_SIZE[1]}")

# 找到所有的 DEM 文件
dem_files = [f for f in os.listdir(raw_dem_dir) if f.endswith('.tif')]
processed_count = 0

for dem_filename in dem_files:
    file_id = dem_filename.split('.')[0] # 提取类似 MT10_0U_38R 的纯ID
    
    # 拼凑出对应的卫星图文件名 (假设你之前存成了 .jpg)
    s2_filename = f"{file_id}.jpg"
    
    raw_dem_path = os.path.join(raw_dem_dir, dem_filename)
    raw_s2_path = os.path.join(raw_s2_dir, s2_filename)
    
    # 确保同时存在对应的卫星图，才进行处理
    if os.path.exists(raw_s2_path):
        
        # 打开原始图片
        dem_img = Image.open(raw_dem_path)
        s2_img = Image.open(raw_s2_path)
        
        # 核心魔法：尺寸对齐 (使用双线性插值 BILINEAR，保证地形高度平滑过渡)
        aligned_dem = dem_img.resize(TARGET_SIZE, resample=Image.Resampling.BILINEAR)
        aligned_s2 = s2_img.resize(TARGET_SIZE, resample=Image.Resampling.BILINEAR)
        
        # 保存到新文件夹
        aligned_dem.save(os.path.join(out_dem_dir, dem_filename))
        aligned_s2.save(os.path.join(out_s2_dir, s2_filename))
        
        processed_count += 1
        print(f"✅ 对齐完成: {file_id}")
    else:
        print(f"⚠️ 找不到对应的卫星图，跳过: {file_id}")

print(f"\n🎉 批量对齐结束！共处理了 {processed_count} 组图片。")
print(f"📁 你的干净数据现在存放在: ./dataset/{REGION_NAME}_Aligned/")