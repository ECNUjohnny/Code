import os

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
    print("正在加载 LangSAM 大模型")
    sam = LangSAM()

    # 路径配置
    input_dir = Path(r"E:\WorkSpace\Data\temp\rgb1")   
    output_dir = Path(r"E:\WorkSpace\Data\temp\mask") # 建议存在新文件夹
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. 定义类别字典 (机器读的绝对数值 ID)
    terrain_classes = {
        "rocks": 1,     # 让 SAM 去找 Prompt 里的“暗色粗糙岩石”
        "dirt": 2,  # 让 SAM 去找 Prompt 里的“红褐色土地”
        "sand": 3   # 让 SAM 去找 Prompt 里的“浅灰色沟壑”
    }

    # 2. 定义彩色调色板 (人眼看的 RGB 颜色)
    # 严格按照 ID (0, 1, 2, 3...) 的顺序排列 [R, G, B, R, G, B...]
    palette = [
        0,   0,   0,     # ID 0: Background (纯黑)
        0,   0,   255,   # ID 1: Water (纯蓝)
        34,  139, 34,    # ID 2: Forest (森林绿)
        255, 0,   0,     # ID 3: Building (亮红)
        128, 128, 128,   # ID 4: Road (灰色)
        210, 180, 140,   # ID 5: Bare Land (黄褐色/沙土色)
    ]
    # PIL 要求调色板必须正好包含 256 个颜色 (256 * 3 = 768 个数值)
    # 所以我们把剩下的全部用 0 (黑色) 补齐
    palette += [0] * (768 - len(palette))

    # 开始批量处理
    image_paths = list(input_dir.glob("*.png"))
    print(f"\n找到 {len(image_paths)} 张卫星图，开始生成彩色掩码图...")

    for img_path in tqdm(image_paths):
        # 创建底图 (全 0 背景)
        id_map = np.zeros((512, 512), dtype=np.uint8)

        for class_name, class_id in terrain_classes.items():
            predict_result = sam.predict(
                image=str(img_path),
                text_prompt=class_name,
                box_threshold=0.1,  
                text_threshold=0.1
            )

            # 2. 安全拦截：如果模型什么都没找到（返回了 None），直接跳过这个类，去算下一个类
            if predict_result is None:
                continue
                
            # 3. 如果成功找到了目标，再把它们解包出来
            masks, boxes, phrases, logits = predict_result

            if masks is not None and len(masks) > 0:
                class_mask = torch.any(masks, dim=0).cpu().numpy()
                id_map[class_mask] = class_id

        # 3. 核心优化：给单通道数据穿上“彩色马甲”
        # 使用 'P' 模式 (Palette) 将 NumPy 数组转为图像
        mask_img = Image.fromarray(id_map, mode='P')
        # 注入调色板
        mask_img.putpalette(palette)
        
        # 保存图片
        mask_img.save(output_dir / f"{img_path.stem}_mask.png")

    print(f"\n全部处理完毕！彩色 Mask 已保存至: {output_dir}")

if __name__ == "__main__":
    main()