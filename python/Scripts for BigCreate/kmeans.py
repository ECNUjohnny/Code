import cv2
import numpy as np
import os

# ==========================================
# 超参数配置 (Hyperparameters)
# ==========================================
INPUT_PATH = r"E:\WorkSpace\Data\test_results_unet_sdxl 7-13 2\0286_Wulong_Karst_Chongqing_China_DEM_y256_x0_base_0_gen_texture.png"
OUTPUT_PATH = r"E:\WorkSpace\Data\test_results_unet_sdxl 7-13 2\kmeans_enhanced.png"
SPLATMAP_OUTPUT_PATH = r"E:\WorkSpace\Data\test_results_unet_sdxl 7-13 2\splatmap_rgba.png"
K_VALUE = 4                          # 依然保持 K=4
SATURATION_SCALE = 4               # 【新增】饱和度放大倍数，2.5 倍足以让红褐色凸显出来
# ==========================================

def generate_splatmap(input_path, output_path, k, sat_scale):
    # 1. 验证文件路径
    if not os.path.exists(input_path):
        print(f"错误：找不到输入文件 '{input_path}'")
        return

    # 2. 读取原始图像 (OpenCV 默认以 BGR 格式读取)
    image_bgr = cv2.imread(input_path)
    if image_bgr is None:
        print(f"错误：无法读取图像。")
        return

    height, width = image_bgr.shape[:2]

    # ==============================================================
    # 【核心修改区：放大特征以欺骗算法】
    # 将原图转为 HSV 空间，专门提取出饱和度 (S) 通道进行暴力拉伸
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(image_hsv)

    # 放大饱和度，并使用 np.clip 确保数值不会溢出 0-255 的安全范围
    s_enhanced = cv2.multiply(s, sat_scale)
    s_enhanced = np.clip(s_enhanced, 0, 255).astype(np.uint8)

    # 将增强后的通道合并，然后转换到 LAB 空间用于精准聚类
    image_hsv_enhanced = cv2.merge([h, s_enhanced, v])
    image_bgr_enhanced = cv2.cvtColor(image_hsv_enhanced, cv2.COLOR_HSV2BGR)
    image_lab_enhanced = cv2.cvtColor(image_bgr_enhanced, cv2.COLOR_BGR2Lab)
    # ==============================================================

    output_folder = os.path.dirname(output_path)
    cv2.imwrite(output_folder + '/enhanced.png', image_bgr_enhanced)

    # 3. 准备聚类数据 (使用增强后的 LAB 图像)
    # 展平为 2D 数组 (像素总数 x 通道数) 且数据类型转为 float32
    pixels_enhanced = image_lab_enhanced.reshape((-1, 3))
    pixels_enhanced = np.float32(pixels_enhanced)

    # 4. 设置 K-Means 停止标准
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    
    print(f"正在对特征放大后的图像进行 LAB 空间的 K={k} 聚类计算...")
    
    # 5. 执行 K-Means
    # 注意：此时算法是被高饱和度图像驱动的，必定会抓出红褐色
    _, labels, _ = cv2.kmeans(
        pixels_enhanced, 
        k, 
        None, 
        criteria, 
        10, 
        cv2.KMEANS_PP_CENTERS 
    )

    # ==============================================================
    # 【核心修改区：回原图提取真实颜色】
    # 算法已经帮我们给每个像素贴好了标签 (labels)，现在我们回原图去算平均色
    pixels_original_bgr = image_bgr.reshape((-1, 3))
    true_centers_bgr = []
    
    for i in range(k):
        # 取出所有被判定为第 i 类的原始像素
        cluster_pixels = pixels_original_bgr[labels.flatten() == i]
        
        # 计算这些真实像素的平均颜色
        if len(cluster_pixels) > 0:
            mean_color = np.mean(cluster_pixels, axis=0)
            true_centers_bgr.append(mean_color)
        else:
            true_centers_bgr.append([0, 0, 0])
            
    true_centers_bgr = np.uint8(true_centers_bgr)
    # ==============================================================

    # 6. 统计每个聚类的像素数量，并按占比降序排序
    label_counts = np.bincount(labels.flatten())
    sorted_indices = np.argsort(label_counts)[::-1]
    
    sorted_centers_bgr = true_centers_bgr[sorted_indices]
    sorted_counts = label_counts[sorted_indices]
    total_pixels = pixels_enhanced.shape[0]

    # 7. 绘制 K 个真实的中心调色板图像
    block_size = 150
    palette_bgr = np.zeros((block_size, block_size * k, 3), dtype=np.uint8)

    print("\n=== 聚类真实颜色结果 (按像素占比排序) ===")
    for i in range(k):
        color_bgr = sorted_centers_bgr[i]
        percentage = (sorted_counts[i] / total_pixels) * 100
        
        print(f"中心 {i+1}: 真实BGR={color_bgr}, 占比: {percentage:.2f}%")
        
        # 将颜色填充到调色板的对应区块中
        start_x = i * block_size
        end_x = (i + 1) * block_size
        palette_bgr[:, start_x:end_x] = color_bgr

    # 8. 保存输出图像
    cv2.imwrite(output_path, palette_bgr)
    print(f"\n成功！基于特征放大的调色板已保存至: '{output_path}'")


if __name__ == "__main__":
    generate_splatmap(INPUT_PATH, OUTPUT_PATH, K_VALUE, SATURATION_SCALE)