import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def visualize_splatmap(image_path):
    # 读取图像
    try:
        img = Image.open(image_path)
        img_array = np.array(img)
    except FileNotFoundError:
        print(f"找不到文件: {image_path}，请确保图片与脚本在同一目录下。")
        return

    # 检查图像通道数
    if len(img_array.shape) == 2:
        print("检测到单通道灰度图。正在使用热力图(伪彩色)进行 RGB 可视化...")
        plt.figure(figsize=(8, 6))
        # 使用 jet 或 viridis 色图将灰度映射为 RGB
        plt.imshow(img_array, cmap='jet') 
        plt.colorbar(label='Weight')
        plt.title("Splatmap (Pseudo-color RGB)")
        plt.axis('off')
        plt.show()
        
    else:
        print("检测到多通道图像。正在分离并可视化 RGB 通道...")
        # 提取 R, G, B 通道

        for i in range(512):
            for j in range(512):
                if img_array[i][j][3] != 0:
                    img_array[i][j][3] = 0
                    img_array[i][j][0] = 255


        r = img_array[:, :, 0]
        g = img_array[:, :, 1]
        b = img_array[:, :, 2]

        # 创建纯黑背景，用于将单通道数据染成对应的红、绿、蓝
        zeros = np.zeros_like(r)
        
        img_r = np.stack([r, zeros, zeros], axis=-1)
        img_g = np.stack([zeros, g, zeros], axis=-1)
        img_b = np.stack([zeros, zeros, b], axis=-1)

        # 检查是否包含 Alpha 通道 (常用于第4种地形纹理)
        has_alpha = img_array.shape[2] == 4
        cols = 5 if has_alpha else 4
        
        # 准备画布
        fig, axes = plt.subplots(1, cols, figsize=(4 * cols, 4))

        # 1. 原始混合图
        axes[0].imshow(img_array[:, :, :3])
        axes[0].set_title("Combined RGB")
        axes[0].axis('off')

        # 2. 红色通道 (通常代表地表材质 1)
        axes[1].imshow(img_r)
        axes[1].set_title("Red Channel (Layer 1)")
        axes[1].axis('off')

        # 3. 绿色通道 (通常代表地表材质 2)
        axes[2].imshow(img_g)
        axes[2].set_title("Green Channel (Layer 2)")
        axes[2].axis('off')

        # 4. 蓝色通道 (通常代表地表材质 3)
        axes[3].imshow(img_b)
        axes[3].set_title("Blue Channel (Layer 3)")
        axes[3].axis('off')

        # 5. Alpha通道 (如果有)
        if has_alpha:
            a = img_array[:, :, 3]
            axes[4].imshow(a, cmap='gray')
            axes[4].set_title("Alpha Channel (Layer 4)")
            axes[4].axis('off')

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # 替换为你的文件名
    visualize_splatmap(r"E:\WorkSpace\Big Create\Data\test_results_unet 8-20 Ice\118_splat_1.png")