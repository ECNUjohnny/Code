import os
import rasterio
from rasterio.windows import Window
import numpy as np

# ================= 1. 配置参数 =================
INPUT_DIR = "D:/File/Research/dataset/Batch_DEM_Outputs"  # 你的原始数据文件夹
OUTPUT_DIR = "D:/File/Research/dataset/Batch_DEM_Outputs2" # 最终数据集输出文件夹
PATCH_SIZE = 256
STRIDE = 64  # 步长 128 代表 50% 的重叠率

os.makedirs(OUTPUT_DIR, exist_ok=True)
tif_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.tif')]

# ================= 2. 核心辅助函数 =================
def save_patch(data_2d, meta, out_path):
    """
    保存 2D 高程矩阵为 TIF 文件。
    rasterio 需要写入 3D 形状 (bands, height, width)，所以这里自动在第 0 维增加一个维度。
    """
    data_3d = np.expand_dims(data_2d, axis=0)
    with rasterio.open(out_path, "w", **meta) as dest:
        dest.write(data_3d)

total_generated = 0

print(f"找到 {len(tif_files)} 张原始数据，开始执行深度切片与全方位增强...\n")

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
                patch_data_3d = src.read(window=window)
                
                # 提取二维高度矩阵用于矩阵变换
                img_2d = patch_data_3d[0] 
                
                # 复制并更新元数据
                patch_meta = src.meta.copy()
                patch_meta.update({
                    "height": PATCH_SIZE, 
                    "width": PATCH_SIZE,
                    "transform": src.window_transform(window)
                })
                
                # ---------- 开始数据增强 ----------
                
                # A. 基础原图 (Base)
                save_patch(img_2d, patch_meta, os.path.join(OUTPUT_DIR, f"{base_name}_y{y}_x{x}_base.tif"))
                total_generated += 1
                
                # B. 水平翻转 (Left-Right Flip)
                flip_lr = np.fliplr(img_2d)
                save_patch(flip_lr, patch_meta, os.path.join(OUTPUT_DIR, f"{base_name}_y{y}_x{x}_flr.tif"))
                total_generated += 1
                
                # C. 垂直翻转 (Up-Down Flip / 上下翻转)
                flip_ud = np.flipud(img_2d)
                save_patch(flip_ud, patch_meta, os.path.join(OUTPUT_DIR, f"{base_name}_y{y}_x{x}_fud.tif"))
                total_generated += 1
                
                # D. 逆时针旋转 90 度 (k=1)
                rot_90 = np.rot90(img_2d, k=1)
                save_patch(rot_90, patch_meta, os.path.join(OUTPUT_DIR, f"{base_name}_y{y}_x{x}_r90.tif"))
                total_generated += 1
                
                # E. 逆时针旋转 180 度 (k=2)
                rot_180 = np.rot90(img_2d, k=2)
                save_patch(rot_180, patch_meta, os.path.join(OUTPUT_DIR, f"{base_name}_y{y}_x{x}_r180.tif"))
                total_generated += 1
                
                # F. 逆时针旋转 270 度 (k=3)
                rot_270 = np.rot90(img_2d, k=3)
                save_patch(rot_270, patch_meta, os.path.join(OUTPUT_DIR, f"{base_name}_y{y}_x{x}_r270.tif"))
                total_generated += 1

print(f"🎉 处理完成！通过步长滑动与物理增强，成功裂变出 {total_generated} 个 {PATCH_SIZE}x{PATCH_SIZE} 训练样本！")