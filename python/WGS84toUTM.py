import os
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import math

# ================= 1. 文件夹路径配置 =================
# INPUT_DIR：你从 NASA AppEEARS 下载解压后的原始 TIF 文件夹
INPUT_DIR = "D:\File\Research\dataset\Test1"   
# OUTPUT_DIR：转换后（单位变为米）的 TIF 文件夹，准备进 Unity 或 ML
OUTPUT_DIR = "D:\File\Research\dataset\Test2"  

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_utm_epsg(lon, lat):
    """根据经纬度自动计算最佳 UTM 投影带的 EPSG 代码"""
    zone = math.floor((lon + 180) / 6) + 1
    epsg_prefix = 32600 if lat >= 0 else 32700
    return epsg_prefix + zone

# ================= 2. 批量处理图像 =================
tif_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.tif')]
print(f"找到 {len(tif_files)} 张从 NASA 下载的原始高程图，开始重投影...\n")

for filename in tif_files:
    in_path = os.path.join(INPUT_DIR, filename)
    out_path = os.path.join(OUTPUT_DIR, filename)
    
    print(f"正在转换: {filename} ...")
    
    with rasterio.open(in_path) as src:
        # 1. 计算图像中心点的经纬度，用来推算 UTM 带
        center_lon = (src.bounds.left + src.bounds.right) / 2
        center_lat = (src.bounds.bottom + src.bounds.top) / 2
        target_epsg = f"EPSG:{get_utm_epsg(center_lon, center_lat)}"
        
        # 2. 计算投影转换后的新尺寸 (width, height) 和仿射变换矩阵 (transform)
        # 这一步是核心：因为地球是圆的，展平后图片的宽高比例会发生物理改变
        transform, width, height = calculate_default_transform(
            src.crs, target_epsg, src.width, src.height, *src.bounds
        )
        
        # 3. 复制原始元数据，并更新为新的坐标系和尺寸
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': target_epsg,
            'transform': transform,
            'width': width,
            'height': height
        })
        
        # 4. 创建新文件并执行像素重投影
        with rasterio.open(out_path, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=target_epsg,
                    # ⚠️ 极其关键：高程地形必须用双线性(bilinear)或三次卷积(cubic)重采样
                    # 绝对不能用默认的最近邻(nearest)，否则山体表面会变成马赛克阶梯！
                    resampling=Resampling.bilinear 
                )
                
        print(f"  -> 成功！已重投影至 {target_epsg} (单位: 米)")

print("\n🎉 全部地形图重投影完成！现在它们可以完美导入 Unity 或用于机器学习了。")