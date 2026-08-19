import cv2
import torch
import os
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

def enhance_terrain_texture(input_path, output_path):
    # 1. 自动检测 GPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"正在使用设备: {device}")

    # 2. 初始化底层模型架构 (针对真实场景的 x4plus 模型)
    # num_in_ch, num_out_ch, num_feat 等是 x4plus 模型的固定超参数
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
    
    # 官方模型权重下载链接 (首次运行会自动下载到环境目录中)
    model_path = './weights/RealESRGAN_x4plus.pth'

    # 3. 实例化放大器
    upsampler = RealESRGANer(
        scale=4,               # 放大倍数 (512 -> 2048)
        model_path=model_path,
        dni_weight=None,
        model=model,
        tile=0,                # 显存优化：如果你显存爆了(OOM)，改成 256 或 512 进行分块推理
        tile_pad=10,           # 分块边缘的 padding，防止拼接缝隙
        pre_pad=0,
        half=True,             # 开启 fp16 半精度推理，大幅提升速度并节省一半显存 (仅限 GPU)
        device=device
    )

    # 4. 读取图像 (OpenCV 默认读取为 BGR 格式)
    print(f"读取纹理图: {input_path} ...")
    img = cv2.imread(input_path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"图片读取失败，请检查路径: {input_path}")

    # 5. 执行推理
    print("正在生成高频细节，请稍候...")
    try:
        # outscale=4 表示最终输出放大 4 倍
        output, _ = upsampler.enhance(img, outscale=4)
    except RuntimeError as error:
        print('超分失败：可能是显存不足。请尝试将上面的 tile 参数设置为 256。')
        print(error)
        return

    # 6. 保存结果
    cv2.imwrite(output_path, output)
    print(f"处理完成！高清纹理已保存至: {output_path}")

if __name__ == '__main__':
    # 将此处的路径替换为你实际存放图片的路径
    input_image = r'E:\WorkSpace\Big Create\Data\test_results_unet 8-16 1\154_3_gen_texture.png'
    output_image = r'E:\WorkSpace\Big Create\Data\test_results_unet 8-16 1\154_3_gen_hyper_texture.png'
    
    # 如果输出文件夹不存在，先创建
    os.makedirs(os.path.dirname(output_image) or '.', exist_ok=True)
    
    enhance_terrain_texture(input_image, output_image)