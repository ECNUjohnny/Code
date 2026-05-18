import os
import numpy as np
import tifffile
import cv2

# 设置你的输入和输出文件夹路径
input_folder = "D:\WorkSpace\Research\dataset\Test2"  # 替换成你的 TIFF 文件夹
output_folder = "D:/WorkSpace/Research/dataset/Test3" # 转换后 PNG 的保存位置

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 获取所有 tif 文件
tif_files = [f for f in os.listdir(input_folder) if f.endswith('.tif')]

for file_name in tif_files:
    input_path = os.path.join(input_folder, file_name)
    output_path = os.path.join(output_folder, file_name.replace('.tif', '.png'))
    
    # 【新增】打印当前正在处理的文件名，这样报错时你就知道是哪个文件的问题了
    #print(f"正在处理: {file_name} ...")
    
    try:
        # 1. 读取高精度 TIFF 数据
        img = tifffile.imread(input_path)
        
        # 将可能存在的 NoData (比如极其负的数值) 设为当前图块的最低海拔
        img[img < -1000] = np.min(img[img >= -1000]) 
        
        # 2. 归一化处理 (映射到 0 到 65535 的 16-bit 范围)
        img_min = np.min(img)
        img_max = np.max(img)
        
        if img_max > img_min:
            img_normalized = (img - img_min) / (img_max - img_min) * 65535.0
        else:
            img_normalized = np.zeros_like(img)
            
        # 3. 转换为 16-bit 无符号整数
        img_16bit = img_normalized.astype(np.uint16)
        
        # 4. 保存为 PNG
        cv2.imwrite(output_path, img_16bit)
        
    except Exception as e:
        # 【新增】如果报错，打印出具体的错误信息并跳过该文件，继续处理下一个
        print(f"❌ 读取或处理文件 {file_name} 时失败，原因: {e}")
        continue
    
print("批量转换完成！")