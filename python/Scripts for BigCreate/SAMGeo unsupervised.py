import os

# 强制缓存路径
os.environ['TORCH_HOME'] = r'D:\Temp\checkpoint'

import numpy as np
from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt  # 新增：用于将 ID 转换为肉眼可见的彩色

# 使用 SamGeo 进行无监督的自动掩码生成
from samgeo import SamGeo

def main():
    print("正在加载 SAM 自动掩码生成大模型...")
    sam = SamGeo(
        model_type="vit_h", 
        automatic=True,
        sam_kwargs={
            "points_per_side": 32,      # 采样点密度
            "pred_iou_thresh": 0.86,    
            "stability_score_thresh": 0.92 
        }
    )

    # 路径配置
    input_dir = Path(r"E:\WorkSpace\Data\test_results_unet_sdxl 7-13 2\0236_Kuqa_Grand_Canyon_Xinjiang_DEM_y256_x0_base_0_gen_texture.png")   
    output_dir = Path(r"E:\WorkSpace\Data\test_results_unet_sdxl 7-13 2")
    output_dir.mkdir(parents=True, exist_ok=True)

    image_paths = list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.png"))
    print(f"\n找到 {len(image_paths)} 张图片，开始无监督提取掩码...")

    for img_path in image_paths:
        print(f"\n--- 正在处理: {img_path.name} ---")
        
        # 1. 核心数据文件 (高位深 TIF)
        output_mask_path = output_dir / f"{img_path.stem}_mask.tif"
        
        sam.generate(
            source=str(img_path),
            output=str(output_mask_path),
            foreground=True, 
            unique=True      # 为每一个独立色块分配唯一的整数 ID
        )
        print(f" 核心数据已保存: {output_mask_path.name}")

        # 2. ================= 核心新增：彩色预览图渲染 =================
        print(" 正在绘制彩色视觉预览图...")
        try:
            # 读取刚刚生成的绝对值很低的 TIF 文件
            mask_tif = Image.open(output_mask_path)
            mask_np = np.array(mask_tif)
            
            # 打印一下模型一共找出了多少个独立区块，让你心里有数
            unique_ids = np.unique(mask_np)
            print(f" 奇迹时刻！大模型在图中一共揪出了 {len(unique_ids) - 1} 个独立物块/建筑！")

            # 利用 matplotlib 的色彩映射（这里用 gist_ncar 调色板，颜色极多且对立性强）
            plt.figure(figsize=(12, 12))
            plt.imshow(mask_np, cmap='gist_ncar')
            plt.axis('off')  # 关掉坐标轴
            
            # 保存为供人类肉眼查看的 PNG 预览图
            preview_path = output_dir / f"{img_path.stem}_preview.png"
            plt.savefig(preview_path, bbox_inches='tight', pad_inches=0, dpi=150)
            plt.close()
            print(f" 彩色预览图已保存: {preview_path.name}")
            
        except Exception as e:
            print(f" 预览图生成失败 (但不影响核心TIF数据): {e}")
        # ==============================================================

    print(f"\n全部处理完毕！快去文件夹查看带有 '_preview.png' 后缀的彩色图吧！")

if __name__ == "__main__":
    main()