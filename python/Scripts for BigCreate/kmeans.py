import cv2
import numpy as np
from PIL import Image
from pathlib import Path

def generate_mask_kmeans():
    input_dir = Path(r"E:\WorkSpace\Data\temp\rgb1")   
    output_dir = Path(r"E:\WorkSpace\Data\temp\mask_kmeans")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 你的调色板
    palette = [
        0,   0,   0,     # 0: 背景
        0,   0,   255,   # 1: Water (不用)
        34,  139, 34,    # 2: Forest (不用)
        255, 0,   0,     # 3: 浅灰沟壑 -> 红色显示
        128, 128, 128,   # 4: 黑色岩石 -> 灰色显示
        210, 180, 140,   # 5: 红褐土地 -> 沙土色显示
    ]
    palette += [0] * (768 - len(palette))

    # 寻找 jpg 和 png
    image_paths = list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.png"))
    
    for img_path in image_paths:
        # 1. 读取图片并转换为 RGB
        img = cv2.imread(str(img_path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # 2. 把 512x512 的二维图片拉平成一维像素点序列
        pixel_values = img.reshape((-1, 3))
        pixel_values = np.float32(pixel_values)
        
        # 3. 配置 K-Means 参数 (设定寻找 3 种主色调)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        k = 3 # 寻找3个类别 (岩石、红土、沟壑)
        _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        # 4. 根据亮度对找到的 3 个颜色排序 (暗=岩石, 中=红土, 亮=沟壑)
        # 这确保了每次生成的 ID 都是固定的，不会乱序
        brightness = np.sum(centers, axis=1)
        sorted_indices = np.argsort(brightness)
        
        # 创建一个映射字典: 将随机的 label 映射到我们想要的 ID (3, 4, 5)
        # 亮度最暗 (岩石) -> ID 4, 亮度居中 (红土) -> ID 5, 亮度最亮 (沟壑) -> ID 3
        label_mapping = {
            sorted_indices[0]: 4, # 最暗 -> 岩石
            sorted_indices[1]: 5, # 居中 -> 红土
            sorted_indices[2]: 3  # 最亮 -> 沟壑
        }
        
        # 5. 组装 ID 掩码图
        labels = labels.flatten()
        mapped_labels = np.array([label_mapping[label] for label in labels], dtype=np.uint8)
        id_map = mapped_labels.reshape(img.shape[:2])
        
        # 6. 涂上调色板并保存
        mask_img = Image.fromarray(id_map, mode='P')
        mask_img.putpalette(palette)
        mask_img.save(output_dir / f"{img_path.stem}_mask.png")
        print(f"成功处理: {img_path.name}")

if __name__ == "__main__":
    generate_mask_kmeans()