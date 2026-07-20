import os
import cv2
import numpy as np
import rasterio
from rasterio.transform import from_origin
from pathlib import Path

def prepare_terrains_for_grass(input_dir, output_dir, max_real_height=2000.0, pixel_size=200.0):
    """
    将 16 位相对高度图批量转化为 GRASS GIS 适用的真实物理尺度 GeoTIFF
    
    :param input_dir: 输入的 PNG 文件夹
    :param output_dir: 输出的 TIF 文件夹
    :param max_real_height: 映射的最高海拔 (米)，决定了地形的陡峭程度
    :param pixel_size: 水平像素分辨率 (米/像素)，对齐 PTRM 论文的 200 米标准
    """
    in_path = Path(input_dir)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    # 筛选 PNG 图像
    image_files = [f for f in in_path.glob("*.png")]
    print(f"找到 {len(image_files)} 张高度图，准备进行物理尺度重映射...")
    
    for img_path in image_files:
        # 1. 强制读取原始 16 位深度
        img = cv2.imread(str(img_path), cv2.IMREAD_UNCHANGED)
        if img is None or img.dtype != np.uint16:
            print(f"跳过无效或非 16位 图像: {img_path.name}")
            continue
            
        # 2. 压缩与重映射：将 [0, 65535] 线性压缩到 [0, max_real_height] 米
        # 转换为 Float32 以保留真实世界海拔精度
        img_float = img.astype(np.float32)
        real_elevation = (img_float / 65535.0) * max_real_height
        
        # 3. 构造地理空间变换矩阵 (Affine Transform)
        # 假设左上角坐标为 (0, 0)，每个像素代表 X和Y 方向的 pixel_size 米
        transform = from_origin(0, 0, pixel_size, pixel_size)
        
        h, w = real_elevation.shape
        out_tif = out_path / f"{img_path.stem}_geo.tif"
        
        # 4. 写入带有物理元数据的 GeoTIFF
        with rasterio.open(
            out_tif,
            'w',
            driver='GTiff',
            height=h,
            width=w,
            count=1,
            dtype=real_elevation.dtype,
            crs='+proj=merc +datum=WGS84', # 赋予一个基础的墨卡托投影
            transform=transform,
        ) as dst:
            dst.write(real_elevation, 1)
            
        print(f"已转换: {out_tif.name} (范围: 0 ~ {max_real_height}米, 像素: {pixel_size}米)")

# ================= 运行转换 =================
INPUT_FOLDER = r"E:\WorkSpace\Data\test_results_unet_sdxl 7-13 2"
OUTPUT_FOLDER = r"E:\WorkSpace\Data\grass_ready_tiffs"

# 这里设定最高峰为 2000 米，你可以根据想要的陡峭度灵活调整
prepare_terrains_for_grass(INPUT_FOLDER, OUTPUT_FOLDER, max_real_height=1000.0)