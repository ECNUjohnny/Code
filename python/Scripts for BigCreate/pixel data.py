import cv2
import numpy as np
from pathlib import Path

def check_image_min_max(folder_path, num_images=5):
    """
    读取文件夹中指定数量的图片，并打印它们的最大值、最小值、数据类型和尺寸。
    """
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        print(f"文件夹不存在或路径错误: {folder_path}")
        return
        
    # 支持的图片格式后缀
    valid_extensions = {'.png', '.jpg', '.jpeg', '.tif', '.tiff'}
    
    # 筛选出所有图片文件
    image_files = [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in valid_extensions]
    
    if not image_files:
        print("文件夹中没有找到支持的图片文件。")
        return
        
    # 截取用户指定数量的图片
    images_to_process = image_files[:num_images]
    
    print(f"共找到 {len(image_files)} 张图片，正在检查前 {len(images_to_process)} 张...\n")
    print("-" * 50)
    
    for img_path in images_to_process:
        # 【核心操作】IMREAD_UNCHANGED 保证 16 位 PNG 或 TIFF 不会被强转为 8 位
        img = cv2.imread(str(img_path), cv2.IMREAD_UNCHANGED)
        
        if img is None:
            print(f"[错误] 无法读取图片: {img_path.name}")
            continue
            
        img_min = np.min(img)
        img_max = np.max(img)
        
        print(f"文件名: {img_path.name}")
        print(f"  ▸ 分辨率: {img.shape}")
        print(f"  ▸ 数据格式: {img.dtype}")
        print(f"  ▸ 最小值: {img_min}")
        print(f"  ▸ 最大值: {img_max}")
        print("-" * 50)

# ================= 运行示例 =================

# 替换为你实际存放测试图或生成图的绝对路径
target_folder = r"E:\WorkSpace\Data\dataset\Yadan\Yadan\0099_Borkou_Mega_Yardang_Sahara_Chad_DEM_y0_x0_base"

# 设定你要检查的数量，比如读取前 10 张图
check_image_min_max(target_folder, num_images=1)