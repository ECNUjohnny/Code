import cv2
import numpy as np
from skimage import color

input = r'E:\WorkSpace\Data\test_results_unet_sdxl 7-13 2\0236_Kuqa_Grand_Canyon_Xinjiang_DEM_y256_x0_base_0_gen_texture.png'
output = r'E:\WorkSpace\Data\test_results_unet_sdxl 7-13 2'

def color_distance_blending(image_path, unity_output=f"{output}/unity_splatmap.png", vis_output=f"{output}/visualization_map.jpg"):
    img = cv2.imread(image_path)
    if img is None:
        print("图片读取失败！")
        return
        
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 抹平高光和阴影噪声
    blurred_img = cv2.GaussianBlur(img_rgb, (31, 31), 0)
    
    # 定义你的目标地貌色板 (RGB)
    palette_rgb = np.array([
        [150,  80,  70],   # 通道 0 (R): 偏红色的岩石
        [ 80, 100,  60],   # 通道 1 (G): 偏绿色的植被/苔藓
        [100,  80,  60],   # 通道 2 (B): 褐色的泥土/普通岩石
        [ 40,  40,  45]    # 通道 3 (A): 暗色缝隙/深色砂石
    ], dtype=np.uint8)

    lab_img = color.rgb2lab(blurred_img)
    palette_lab = color.rgb2lab(palette_rgb.reshape(1, 4, 3)).reshape(4, 3)

    h, w, c = lab_img.shape
    pixels_lab = lab_img.reshape(-1, 3)

    distances = np.linalg.norm(pixels_lab[:, np.newaxis, :] - palette_lab[np.newaxis, :, :], axis=2)
    labels = np.argmin(distances, axis=1)
    segmented_img = labels.reshape(h, w)

    channels = []
    kernel = np.ones((15, 15), np.uint8)
    color_names = ["偏红岩石", "绿色植被", "褐色泥土", "暗色砂石"]
    
    for i in range(4):
        mask = (segmented_img == i).astype(np.uint8) * 255
        
        # 填海造陆去噪点
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # 边缘羽化
        soft_mask = cv2.GaussianBlur(mask, (21, 21), 0)
        channels.append(soft_mask)
        
        coverage = np.count_nonzero(mask) / (h * w) * 100
        print(f"[{color_names[i]}] 提取完成: 覆盖率 {coverage:.2f}%")

    # ================= 1. 生成给 Unity 用的数据图 (RGBA) =================
    # OpenCV 是 BGR 顺序，所以按 B, G, R, A 传入
    rgba_splatmap = cv2.merge((channels[2], channels[1], channels[0], channels[3]))
    cv2.imwrite(unity_output, rgba_splatmap)
    print(f"[给引擎] Unity Splatmap 已保存: {unity_output}")
    
    # ================= 2. 生成给你看的可视化图 (RGB) =================
    # 创建一个纯黑的画布
    vis_img = np.zeros((h, w, 3), dtype=np.float32)
    
    # 为 4 个通道定义极其鲜艳的代表色 (OpenCV 格式: BGR)
    # 通道0(红) -> 亮红色, 通道1(绿) -> 亮绿色, 通道2(蓝) -> 亮蓝色, 通道3(Alpha) -> 明黄色
    vis_colors = [
        [0, 0, 255],     # 红
        [0, 255, 0],     # 绿
        [255, 0, 0],     # 蓝
        [0, 255, 255]    # 黄
    ]
    
    # 根据羽化后的权重，把这 4 种颜色叠加上去
    for i in range(4):
        weight = channels[i].astype(np.float32) / 255.0
        for c_idx in range(3):
            vis_img[:, :, c_idx] += weight * vis_colors[i][c_idx]
            
    # 限制数值范围并保存
    vis_img = np.clip(vis_img, 0, 255).astype(np.uint8)
    cv2.imwrite(vis_output, vis_img)
    print(f"[给你看] 可视化色彩分布图 已保存: {vis_output}")

# 运行代码
color_distance_blending(input)