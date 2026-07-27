import cv2
import numpy as np
import os

# ==========================================
# 超参数配置 (Hyperparameters)
# 请直接在此处修改你的文件路径和 K 值
# ==========================================
INPUT_PATH = r"E:\WorkSpace\Data\test_results_unet_sdxl 7-13 2\0286_Wulong_Karst_Chongqing_China_DEM_y256_x0_base_0_gen_texture.png"     # 输入图片的路径 (确保图片与脚本在同目录，或使用绝对路径)
OUTPUT_PATH = r"E:\WorkSpace\Data\test_results_unet_sdxl 7-13 2\kmeans.png" # 输出调色板图片的路径
K_VALUE = 4                          # K-Means 的 K 值 (聚类中心数量，建议设为 3 或 4)
# ==========================================

def extract_dominant_colors(input_path, output_path, k):
    # 1. 验证文件路径
    if not os.path.exists(input_path):
        print(f"错误：找不到输入文件 '{input_path}'，请检查 INPUT_PATH 的设置。")
        return

    # 2. 读取图像 (OpenCV 默认以 BGR 格式读取)
    image = cv2.imread(input_path)
    if image is None:
        print(f"错误：无法读取图像，请检查文件是否损坏或格式是否受支持。")
        return

    # 3. 数据预处理
    # K-Means 算法要求输入为 2D 数组 (像素总数 x 通道数) 且数据类型为 float32
    pixels = image.reshape((-1, 3))
    pixels = np.float32(pixels)

    # 4. 设置 K-Means 停止标准 (Criteria)
    # 达到 100 次迭代，或者聚类中心移动距离小于 0.2 时停止
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    
    print(f"正在对图像 '{input_path}' 进行 K={k} 的 K-Means 聚类计算...")
    
    # 5. 执行 K-Means
    # flags=cv2.KMEANS_PP_CENTERS 表示使用 K-Means++ 算法初始化中心，能有效避免陷入局部最优
    _, labels, centers = cv2.kmeans(
        pixels, 
        k, 
        None, 
        criteria, 
        10, # 使用不同的初始中心点执行 10 次算法，并返回最佳结果
        cv2.KMEANS_PP_CENTERS 
    )

    # 将计算得到的浮点数中心转换回 8 位无符号整数 (0-255)
    centers = np.uint8(centers)

    # 6. 统计每个聚类的像素数量，并按占比降序排序
    label_counts = np.bincount(labels.flatten())
    sorted_indices = np.argsort(label_counts)[::-1]
    
    sorted_centers = centers[sorted_indices]
    sorted_counts = label_counts[sorted_indices]
    total_pixels = pixels.shape[0]

    # 7. 绘制 K 个中心的调色板图像
    # 设定调色板的尺寸：高度 150 像素，宽度为 K * 150 像素
    block_size = 150
    palette = np.zeros((block_size, block_size * k, 3), dtype=np.uint8)

    print("\n=== 聚类颜色中心结果 (按像素占比排序) ===")
    for i in range(k):
        color = sorted_centers[i]
        percentage = (sorted_counts[i] / total_pixels) * 100
        
        # 注意：OpenCV 打印出的 color 数组顺序是 [B, G, R]
        print(f"中心 {i+1}: BGR={color}, 占比: {percentage:.2f}%")
        
        # 将颜色填充到调色板的对应区块中
        start_x = i * block_size
        end_x = (i + 1) * block_size
        palette[:, start_x:end_x] = color

    # 8. 保存输出图像
    cv2.imwrite(output_path, palette)
    print(f"\n成功！颜色中心调色板已保存至: '{output_path}'")

if __name__ == "__main__":
    # 直接将头部配置的超参数传入函数执行
    extract_dominant_colors(INPUT_PATH, OUTPUT_PATH, K_VALUE)