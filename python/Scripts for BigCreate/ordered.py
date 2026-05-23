import os
import shutil
from pathlib import Path
from tqdm import tqdm
import random

# ==========================================
# 1. 配置区 (路径与规则)
# ==========================================
# 输入的根目录 (截图中的路径)
INPUT_DIR = r"D:\WorkSpace\Data\outputs\outputs"

# 输出的根目录 (它会在这个路径下自动新建三个子文件夹)
OUTPUT_BASE = r"D:\WorkSpace\Data\unet"
FILTER = r"D:\WorkSpace\Data\outputs\outputs\has_urban"

DIR_DEM = os.path.join(OUTPUT_BASE, "dem")
DIR_RGB = os.path.join(OUTPUT_BASE, "rgb")
DIR_TXT = os.path.join(OUTPUT_BASE, "txt")

mp = {}

def load_filter():

    filter_path = Path(FILTER)

    subdirs = [d for d in filter_path.iterdir() if d.is_dir()]

    for subdir in subdirs:

        mp[subdir.name] = 1

def process_dataset():
    # 自动创建目标文件夹
    os.makedirs(DIR_DEM, exist_ok=True)
    os.makedirs(DIR_RGB, exist_ok=True)
    os.makedirs(DIR_TXT, exist_ok=True)

    load_filter()

    input_path = Path(INPUT_DIR)
    # 获取所有的子文件夹 (例如: 0001_Binggou_Danxia_...)
    subdirs = [d for d in input_path.iterdir() if d.is_dir()]

    print(f"发现 {len(subdirs)} 个数据子文件夹，开始提取与重组...\n")

    # ==========================================
    # 2. 核心遍历与提取逻辑
    # ==========================================
    for subdir in tqdm(subdirs, desc="处理进度"):
        folder_name = subdir.name # 获取外层文件夹的名字，用作未来的统一文件名
        
        if folder_name[0] != '0':
            
            continue

        if folder_name in mp:

            continue

        # 遍历当前子文件夹内的所有文件
        for file_path in subdir.iterdir():
            

            if not file_path.is_file():
                continue

            filename_lower = file_path.name.lower()
            extension = file_path.suffix.lower() # 获取后缀，如 .png, .txt

            # 核心魔法：使用子文件夹的名字作为新的文件名，防止覆盖！
            # 例如最终变为: 0001_Binggou_Danxia_Gansu_DEM_y0_x0.png
            new_filename = f"{folder_name}{extension}"

            # ----------------------------------------
            # 规则 A：提取文本描述
            # ----------------------------------------
            if extension in ['.txt', '.json']:
                target_path = os.path.join(DIR_TXT, new_filename)

                shutil.copy2(file_path, target_path)

            # ----------------------------------------
            # 规则 B：区分并提取两种图片 (高度图 vs 纹理图)
            # ----------------------------------------
            elif extension in ['.png', '.jpg', '.jpeg', '.tif', '.tiff']:
                
                # 请根据你子文件夹里图片实际的名字修改这里的关键词！
                # 假设：高度图的文件名里带有 "dem" 或 "height" 字符
                if 'dem' in filename_lower or 'height' in filename_lower:
                    target_path = os.path.join(DIR_DEM, new_filename)

                    shutil.copy2(file_path, target_path)
                
                # 假设：纹理卫星图的文件名里带有 "rgb" 或 "texture" 或 "sat" 字符
                elif 'rgb' in filename_lower or 'texture' in filename_lower or 'sat' in filename_lower:
                    target_path = os.path.join(DIR_RGB, new_filename)
                
                    shutil.copy2(file_path, target_path)
                
                else:
                    # 如果你的两张图片命名没有规律（比如一张叫 1.png 一张叫 2.png），
                    # 会走到这里，你需要修改上面的 if 关键词来精确匹配。
                    pass


    print(f"\n提取完成! 数据已分类保存在: {OUTPUT_BASE}")

if __name__ == '__main__':
    
    process_dataset()