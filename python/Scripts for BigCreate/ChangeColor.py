import cv2
import numpy as np
import os
import argparse
from tqdm import tqdm  # 新增：导入进度条库

# ==========================================
# 配置区
# ==========================================

# 1. 预设文件夹路径 (请在这里修改为你真实的常用路径)
DEFAULT_INPUT = r"D:\WorkSpace\Data\temp\rgb"            # 默认读取的文件夹
DEFAULT_OUTPUT = r"D:\WorkSpace\Data\temp\rgb_1"    # 默认保存的文件夹

# 2. 定义“丹霞红”的 RGB 颜色值
DANXIA_RGB = (160, 40, 40)

# 3. 融合比例配置 (0.0 - 1.0)
ORIGINAL_ALPHA = 0.3
RED_ALPHA = 0.7

# ==========================================
# 核心逻辑
# ==========================================

def process_images(input_dir, output_dir):
    danxia_bgr = (DANXIA_RGB[2], DANXIA_RGB[1], DANXIA_RGB[0])

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"已创建输出目录: {output_dir}")

    supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')

    # 先筛选出所有支持的文件，为了给进度条提供准确的总数
    files_to_process = [f for f in os.listdir(input_dir) if f.lower().endswith(supported_extensions)]
    
    if not files_to_process:
        print(f"在 '{input_dir}' 中没有找到支持的图片文件。")
        return

    print(f"输入路径: {input_dir}")
    print(f"输出路径: {output_dir}")
    print("-" * 50)

    # 核心魔法：使用 tqdm 包装循环，生成丝滑的进度条
    for filename in tqdm(files_to_process, desc="渲染进度", unit="张"):
        img_path = os.path.join(input_dir, filename)
        
        img = cv2.imread(img_path)
        if img is None:
            # 遇到错误时，用 tqdm.write 打印，防止打断原本完美的进度条画面
            tqdm.write(f"无法读取图片: {filename}")
            continue

        h, w, c = img.shape
        red_layer = np.full((h, w, c), danxia_bgr, dtype=np.uint8)
        
        # 融合图片
        result_img = cv2.addWeighted(img, ORIGINAL_ALPHA, red_layer, RED_ALPHA, 0)

        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, result_img)

    print(f"\n渲染完毕！成功处理了 {len(files_to_process)} 张图片。")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="丹霞地貌红色渲染脚本 (带进度条与默认路径)")
    
    # ✨ 关键修改：去掉了 required=True，加入了 default=预设变量
    parser.add_argument('--input', '-i', type=str, default=DEFAULT_INPUT, help="输入文件夹路径 (默认使用代码内预设)")
    parser.add_argument('--output', '-o', type=str, default=DEFAULT_OUTPUT, help="输出文件夹路径 (默认使用代码内预设)")

    args = parser.parse_args()

    process_images(args.input, args.output)