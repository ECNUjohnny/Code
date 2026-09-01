from pathlib import Path
from PIL import Image
import os

INPUT = r'D:\Temp\Photos for Essay\supplemental'
OUTPUT = r'D:\Temp\Photos for Essay\Yardang\Image Sequence_169_21h52m.png'

def add_white_background(input_path, output_path):
    # 打开图片
    imgs = []

    imgs = [f for f in Path(input_path).rglob('*Image*') if f.is_file()]

    for input in imgs:    
        img = Image.open(input)
        
        # 检查并处理带有透明通道的图片 (RGBA, LA, 或带透明信息的 P 模式)
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            # 统一转为 RGBA 模式
            img_rgba = img.convert("RGBA")
            # 创建一张相同尺寸的纯白底图 (RGB 模式)
            white_bg = Image.new("RGB", img_rgba.size, (255, 255, 255))
            # 将原图贴到白底上，使用 Alpha 通道作为遮罩 (mask)
            white_bg.paste(img_rgba, mask=img_rgba.split()[3]) 
            img = white_bg
        elif img.mode != 'RGB':
            # 处理其他非 RGB 格式（防止报错）
            img = img.convert('RGB')
            
        # 直接保存为原尺寸的 PNG 格式，不进行任何画质压缩
        img.save(input.resolve(), "PNG")
        print(f"处理完成！白底已生成，原始尺寸保持为: {img.size}")

# 使用示例
# compress_and_fix_background("你的原图带透明.png", "最终白底论文图.jpg")

if __name__ == '__main__':
    add_white_background(INPUT, INPUT)
