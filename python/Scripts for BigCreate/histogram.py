import cv2
import matplotlib.pyplot as plt
import os

# ==========================================
# 超参数配置区 (Hyperparameters)
# ==========================================

# 1. 输入图像的路径 (请确保图片与脚本在同级目录，或提供绝对路径)
INPUT_IMAGE_PATH = r"E:\WorkSpace\Data\test_results_unet_sdxl 7-13 2\0286_Wulong_Karst_Chongqing_China_DEM_y256_x0_base_0_gen_texture.png"

# 2. 输出直方图的保存路径
OUTPUT_HISTOGRAM_PATH = r"E:\WorkSpace\Data\test_results_unet_sdxl 7-13 2\histogram.png"

# ==========================================

def generate_histogram(input_path, output_path):
    # 1. 读取图像
    img = cv2.imread(input_path)
    if img is None:
        print(f"错误: 无法读取输入图像，请检查路径是否正确: {input_path}")
        return
    
    # 2. 色彩空间转换
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 3. 创建图表画布 (包含左右两张子图)
    plt.figure(figsize=(14, 6))

    # ---- 子图 1: RGB 直方图 ----
    plt.subplot(1, 2, 1)
    plt.title("RGB Color Histogram")
    plt.xlabel("Pixel Intensity (0-255)")
    plt.ylabel("Frequency")
    
    colors = ('r', 'g', 'b')
    for i, col in enumerate(colors):
        hist = cv2.calcHist([img_rgb], [i], None, [256], [0, 256])
        plt.plot(hist, color=col, alpha=0.8)
        plt.xlim([0, 256])
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # ---- 子图 2: Hue (色相) 直方图 ----
    plt.subplot(1, 2, 2)
    plt.title("Hue (HSV) Channel Histogram - For K-Means Analysis")
    plt.xlabel("Hue Value (0-179 in OpenCV)")
    plt.ylabel("Frequency")
    
    hist_hue = cv2.calcHist([img_hsv], [0], None, [180], [0, 180])
    plt.plot(hist_hue, color='purple', linewidth=2)
    plt.xlim([0, 180])
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 4. 调整布局并保存输出
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"分析完成！直方图已成功保存至: {output_path}")

if __name__ == "__main__":
    # 如果输出路径的文件夹不存在，自动创建
    output_dir = os.path.dirname(OUTPUT_HISTOGRAM_PATH)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建输出目录: {output_dir}")

    # 执行分析，直接调用顶部的超参数
    generate_histogram(INPUT_IMAGE_PATH, OUTPUT_HISTOGRAM_PATH)