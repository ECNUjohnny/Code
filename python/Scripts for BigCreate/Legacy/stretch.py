import os
import rasterio
from rasterio.enums import Resampling

# 1. 设置输入和输出文件夹
# input_folder 填入你之前下载好的那些小 TIF 图的文件夹
input_folder = "D:/File/Research/dataset/Batch_DEM_Outputs" 
output_folder = "D:/File/Research/dataset/Batch_DEM_Outputs1"
os.makedirs(output_folder, exist_ok=True)

# 2. 设定目标分辨率 (Unity 地形常用的 1024x1024)
TARGET_WIDTH = 1024
TARGET_HEIGHT = 1024

# 3. 获取文件夹下所有的 .tif 文件
tif_files = [f for f in os.listdir(input_folder) if f.endswith('.tif')]

print(f"找到 {len(tif_files)} 个高程图，准备开始重采样拉伸至 1024x1024...\n")

# 4. 开始循环处理
for filename in tif_files:
    in_path = os.path.join(input_folder, filename)
    out_path = os.path.join(output_folder, filename)
    
    print(f"正在处理: {filename}")
    
    with rasterio.open(in_path) as src:
        # 【核心步骤1：重采样读取】
        # 使用双线性插值 (Bilinear) 或 三次卷积 (Cubic)
        # 这对于地形极其重要！它能保证拉伸后山坡依然平滑，而不会出现马赛克阶梯
        data = src.read(
            out_shape=(src.count, TARGET_HEIGHT, TARGET_WIDTH),
            resampling=Resampling.bilinear 
        )
        
        # 【核心步骤2：重新计算地理坐标仿射变换】
        # 这一步是为了保证虽然像素变多了，但这张图在地球上的经纬度范围不变
        transform = src.transform * src.transform.scale(
            (src.width / TARGET_WIDTH),
            (src.height / TARGET_HEIGHT)
        )
        
        # 【核心步骤3：更新元数据并写入新文件】
        kwargs = src.meta.copy()
        kwargs.update({
            'transform': transform,
            'width': TARGET_WIDTH,
            'height': TARGET_HEIGHT
        })
        
        with rasterio.open(out_path, 'w', **kwargs) as dst:
            dst.write(data)

print("\n🎉 全部处理完成！你的 1024x1024 标准地形图已准备就绪。")