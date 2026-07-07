import os

# 强制缓存路径
os.environ['TORCH_HOME'] = r'D:\Temp\checkpoint'

import torch
import numpy as np
from PIL import Image
from pathlib import Path
from tqdm import tqdm

from transformers.models.bert.modeling_bert import BertModel
if not hasattr(BertModel, 'get_head_mask'):
    # 塞入一个空函数，防止 GroundingDINO 报错
    BertModel.get_head_mask = lambda self, *args, **kwargs: None

# 导入 SAM-Geo 的文本分割模块
from samgeo.text_sam import LangSAM

def main():
    print("正在加载 LangSAM 大模型...")
    sam = LangSAM()

    # 路径配置 (建议改成你存放真实卫星图的文件夹)
    input_dir = Path(r"E:\WorkSpace\Data\temp\rgb1")   
    output_dir = Path(r"E:\WorkSpace\Data\temp\mask")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. 针对【真实卫星图】的类别字典
    # 使用最基础、清晰的英文名词，大模型对这些词的理解最准确
    terrain_classes = {
        "grey street": 4,      # 找浅灰色的街道/马路 (替代 road)
        "green grass": 2,      # 找绿色的草地 (替代 grass)
        "tree canopy": 2,      # 找树冠 (替代 tree，大模型更懂俯视的树冠)
        "dark roof": 3,        # 找深色屋顶 (完美替代 house)
    }

    # 2. 定义彩色调色板 (和上面的 ID 完美对应)
    palette = [
        0,   0,   0,     # ID 0: Background (纯黑)
        0,   0,   255,   # ID 1: Water (纯蓝)
        34,  139, 34,    # ID 2: Forest (森林绿)
        255, 0,   0,     # ID 3: Building (亮红)
        128, 128, 128,   # ID 4: Road (灰色) - 这里留空占位
        210, 180, 140,   # ID 5: Bare Land (黄褐色/沙土色)
    ]
    palette += [0] * (768 - len(palette))

    # 3. 核心修复：同时寻找 JPG 和 PNG
    image_paths = list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.png"))
    print(f"\n找到 {len(image_paths)} 张真实卫星图，开始提取语义掩码...")

    

    for img_path in image_paths:
        print(f"\n--- 正在处理: {img_path.name} ---")
        
        # 1. 核心修复：动态读取真实图片的宽高，避免尺寸不匹配的隐藏 Bug！
        with Image.open(img_path) as img:
            w, h = img.size
        id_map = np.zeros((h, w), dtype=np.uint8)

        for class_name, class_id in terrain_classes.items():
            print(f" AI 正在寻找: '{class_name}' ... ", end="")
            
            predict_result = sam.predict(
                image=str(img_path),
                text_prompt=class_name,
                box_threshold=0.10,  # 适中阈值
                text_threshold=0.10
            )

            if predict_result is None:
                print(f"失败 (大模型没认出来)")
                continue
                
            masks, boxes, phrases, logits = predict_result

            if masks is not None and len(masks) > 0:
                print(f"成功! 抓取到了 {len(masks)} 块区域")
                class_mask = torch.any(masks, dim=0).cpu().numpy()
                id_map[class_mask] = class_id
            else:
                print(f"失败 (找到了边框，但拒绝生成掩码)")

        mask_img = Image.fromarray(id_map, mode='P')
        mask_img.putpalette(palette)
        mask_img.save(output_dir / f"{img_path.stem}_mask.png")

    print(f"\n全部处理完毕.请去文件夹查看。")

if __name__ == "__main__":
    main()