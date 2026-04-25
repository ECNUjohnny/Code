import os
import rasterio
from rasterio.windows import Window
import numpy as np

# ================= 1. 配置参数 =================
# ⚠️ 注意修改这里的输入和输出路径，避免覆盖你的高度图数据
INPUT_DIR = "D:\File\Research\dataset\RGB from CDSE"  
OUTPUT_DIR = "D:\File\Research\dataset\Test3_RGB" 
PATCH_SIZE = 256
STRIDE = 64 # 步长 64

os.makedirs(OUTPUT_DIR, exist_ok=True)
tif_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.tif')]

# ================= 2. 核心辅助函数 =================
def save_patch(data_3d, meta, out_path):
    """
    保存多通道矩阵为 TIF 文件。
    因为 data_3d 已经是 (bands, height, width) 的形状，直接写入即可，无需 expand_dims。
    """
    with rasterio.open(out_path, "w", **meta) as dest:
        dest.write(data_3d)

total_generated = 0

print(f"找到 {len(tif_files)} 张 RGB 卫星图，开始执行深度切片与全方位增强...\n")

# ================= 3. 执行流水线 =================
for filename in tif_files:
    in_path = os.path.join(INPUT_DIR, filename)
    base_name = os.path.splitext(filename)[0]
    
    with rasterio.open(in_path) as src:
        width, height = src.width, src.height
        
        # 尺寸检查
        if width < PATCH_SIZE or height < PATCH_SIZE: 
            continue
        
        # 使用 Stride 计算滑动网格的坐标系
        x_offsets = list(range(0, width - PATCH_SIZE + 1, STRIDE))
        y_offsets = list(range(0, height - PATCH_SIZE + 1, STRIDE))
        
        for y in y_offsets:
            for x in x_offsets:
                # 1. 切取原始基础窗口
                window = Window(col_off=x, row_off=y, width=PATCH_SIZE, height=PATCH_SIZE)
                # 读取出来的形状是 (bands, height, width)，对于 RGB 是 (3, 256, 256)
                patch_data_3d = src.read(window=window) 
                
                # 复制并更新元数据
                patch_meta = src.meta.copy()
                patch_meta.update({
                    "height": PATCH_SIZE, 
                    "width": PATCH_SIZE,
                    "transform": src.window_transform(window)
                })
                
                # ---------- 开始数据增强 ----------
                # 注意：rasterio 的数据排列是 (通道数, Y轴/高度, X轴/宽度)
                # 因此 axis=1 是上下翻转，axis=2 是左右翻转
                
                # A. 基础原图 (Base)
                save_patch(patch_data_3d, patch_meta, os.path.join(OUTPUT_DIR, f"{base_name}_y{y}_x{x}_base.tif"))
                total_generated += 1
                
                # B. 水平翻转 (Left-Right Flip) - 指定翻转 X 轴 (axis=2)
                flip_lr = np.flip(patch_data_3d, axis=2)
                save_patch(flip_lr, patch_meta, os.path.join(OUTPUT_DIR, f"{base_name}_y{y}_x{x}_flr.tif"))
                total_generated += 1
                
                # C. 垂直翻转 (Up-Down Flip / 上下翻转) - 指定翻转 Y 轴 (axis=1)
                flip_ud = np.flip(patch_data_3d, axis=1)
                save_patch(flip_ud, patch_meta, os.path.join(OUTPUT_DIR, f"{base_name}_y{y}_x{x}_fud.tif"))
                total_generated += 1
                
                """
                # D. 逆时针旋转 90 度 (在最后两个维度即空间维度上旋转)
                rot_90 = np.rot90(patch_data_3d, k=1, axes=(1, 2))
                save_patch(rot_90, patch_meta, os.path.join(OUTPUT_DIR, f"{base_name}_y{y}_x{x}_r90.tif"))
                total_generated += 1
                
                # E. 逆时针旋转 180 度
                rot_180 = np.rot90(patch_data_3d, k=2, axes=(1, 2))
                save_patch(rot_180, patch_meta, os.path.join(OUTPUT_DIR, f"{base_name}_y{y}_x{x}_r180.tif"))
                total_generated += 1
                
                # F. 逆时针旋转 270 度
                rot_270 = np.rot90(patch_data_3d, k=3, axes=(1, 2))
                save_patch(rot_270, patch_meta, os.path.join(OUTPUT_DIR, f"{base_name}_y{y}_x{x}_r270.tif"))
                total_generated += 1
                """

print(f"🎉 RGB 处理完成！共成功裂变出 {total_generated} 个 {PATCH_SIZE}x{PATCH_SIZE} 卫星图训练样本！")