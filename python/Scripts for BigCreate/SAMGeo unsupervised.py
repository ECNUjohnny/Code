import os

# 强制缓存路径
os.environ['TORCH_HOME'] = r'D:\Temp\checkpoint'

import numpy as np
from PIL import Image
from pathlib import Path
import cv2

# 使用 SamGeo 进行无监督的自动掩码生成
from samgeo import SamGeo

UNITY_TEXTURE_FOLDERS = {
    "Green": np.array([38, 78, 24]),       # 对应 pfdh2js
    "Grey": np.array([122, 122, 115]),     # 对应 vh3nfijo
    "Red": np.array([153, 84, 64]),        # 对应 venoehv
    "Red1": np.array([156, 107, 88]),      # 对应 vepxaa1cc
    "Red2": np.array([126, 56, 36]),       # 对应 wijbfj1bw
    "White": np.array([226, 230, 235]),    # 对应 uephfgudy
    "Brown": np.array([116, 84, 69])       # 对应 wdvbfiy
}

# 格式： "文件夹名": (Splatmap序号, 通道序号)
# 序号说明：Splatmap序号 (0或1)，通道序号 (0=R, 1=G, 2=B, 3=A)
CHANNEL_MAPPING = {
    "Green": (0, 0),    # 第1张图，R 通道
    "Grey":  (0, 1),    # 第1张图，G 通道
    "Red":   (0, 2),    # 第1张图，B 通道
    "Red1":  (0, 3),    # 第1张图，A 通道
    "Red2":  (1, 0),    # 第2张图，R 通道
    "White": (1, 1),    # 第2张图，G 通道
    "Brown": (1, 2)     # 第2张图，B 通道
}

def get_matching_folder(bgr_color):
    """根据输入的 BGR 颜色，返回最接近的 Unity 文件夹名称"""
    rgb_color = np.array([bgr_color[2], bgr_color[1], bgr_color[0]])
    
    min_distance = float('inf')
    best_folder = None
    
    for folder_name, standard_rgb in UNITY_TEXTURE_FOLDERS.items():
        # 计算欧氏距离找最近似的固定颜色
        distance = np.linalg.norm(rgb_color - standard_rgb)
        if distance < min_distance:
            min_distance = distance
            best_folder = folder_name
            
    return best_folder

def main():
    print("正在加载 SAM 自动掩码生成大模型...")
    sam = SamGeo(
        model_type="vit_h", 
        automatic=True,
        sam_kwargs={
            "points_per_side": 64,      
            "pred_iou_thresh": 0.7,    
            "stability_score_thresh": 0.8 
        }
    )

    input_dir = Path(r"E:\WorkSpace\Data\temp\rgb")   
    output_dir = Path(r"E:\WorkSpace\Data\temp\mask")
    output_dir.mkdir(parents=True, exist_ok=True)

    image_paths = list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.png"))
    print(f"\n找到 {len(image_paths)} 张图片，开始无监督提取掩码...")

    for img_path in image_paths:
        print(f"\n--- 正在处理: {img_path.name} ---")
        
        output_mask_path = output_dir / f"{img_path.stem}_mask.tif"
        
        sam.generate(
            source=str(img_path),
            output=str(output_mask_path),
            foreground=True, 
            unique=True      
        )
        print(f" 核心数据已保存: {output_mask_path.name}")

        print(" 正在计算色彩距离并映射 Unity 材质通道...")
        try:
            mask_tif = Image.open(output_mask_path)
            mask_np = np.array(mask_tif)
            
            unique_ids = np.unique(mask_np)
            print(f" 大模型在图中一共揪出了 {len(unique_ids) - 1} 个独立物块/建筑！")

            image_bgr = cv2.imread(str(img_path))
            if image_bgr is None:
                print('Cannot read this texture\n')
                continue 

            image_lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2Lab)
            height, width = image_bgr.shape[:2]

            # 初始化两张全黑的 Splatmap，维度为 (H, W, 4)，数据类型 uint8 (0-255)
            splatmaps = [
                np.zeros((height, width, 4), dtype=np.uint8), # splatmap_0
                np.zeros((height, width, 4), dtype=np.uint8)  # splatmap_1
            ]

            print(f" 正在提取特征并分配材质通道...")
            for id in unique_ids:

                mask = (mask_np == id)
                pixels = image_lab[mask]
                mean_color = np.mean(pixels, axis=0)
                mean_color_1x1 = np.uint8([[mean_color]])
                mean_color_bgr = cv2.cvtColor(mean_color_1x1, cv2.COLOR_Lab2BGR)[0][0]
                
                # 寻找最近似的基准颜色分类
                best_folder = get_matching_folder(mean_color_bgr)
                
                # 查表，获取该类别对应的图层序号和通道序号
                splat_idx, channel_idx = CHANNEL_MAPPING[best_folder]
                
                # 在对应的 Splatmap 通道上，将该区块权重涂满 (255)
                splatmaps[splat_idx][mask, channel_idx] = 255

            # 保存 Splatmap
            print(" 正在导出 Unity 标准 Control Textures...")
            for s_idx, splat_data in enumerate(splatmaps):
                # OpenCV 默认保存通道顺序为 BGRA，进行翻转以适配正常 RGBA 读取逻辑
                splat_bgra = cv2.cvtColor(splat_data, cv2.COLOR_RGBA2BGRA)
                
                out_path = output_dir / f'{img_path.stem}_splatmap_{s_idx}.png'
                cv2.imwrite(str(out_path), splat_bgra)
            
            print(f" 成功导出 2 张拼接通道遮罩图！")

        except Exception as e:
            print(f" 处理过程中出现异常: {e}")

    print(f"\n全部处理完毕！")

if __name__ == "__main__":
    main()