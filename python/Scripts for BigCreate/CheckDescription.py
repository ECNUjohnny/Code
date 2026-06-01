import cv2
import numpy as np
import os
import argparse
from tqdm import tqdm  # 新增：导入进度条库
import os
import shutil
from pathlib import Path

# ==========================================
# 配置区
# ==========================================

# 1. 预设文件夹路径 (请在这里修改为你真实的常用路径)
INPUT = r"D:\WorkSpace\Data\IceMountain\IceMountain"  # 默认保存的文件夹

def check():

    input_path = Path(INPUT)

    # print(1)

    subdirs = [d for d in input_path.iterdir() if d.is_dir]

    file_cnt = 0

    for subdir in tqdm(subdirs, desc="processing"):

        if subdir.name[0] != '0':
            continue

        for file_path in subdir.iterdir():

            filename = file_path.name.lower()

            if "description" in filename:
                
                file_info = os.path.getsize(file_path)

                file_cnt += 1

                if file_info < 100:

                    print(filename)

    print(file_cnt)

if __name__ == '__main__':

    check()