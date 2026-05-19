import numpy as np
from PIL import Image
import os

# ==========================================
# 1. 替换为你随便一张待训练的 DEM 图片路径
# ==========================================
# 可以是 .png，也可以是 .tif
image_path = r"D:\WorkSpace\Data\unet\dem\0125_Jianglang_Mountain_Zhejiang_DEM_y512_x512_base.png" 

def check_image_data(path):
    if not os.path.exists(path):
        print(f"❌ 找不到文件: {path}")
        return

    try:
        # 读取图片
        img = Image.open(path)
        
        # 转换为 numpy 数组
        data = np.array(img)
        
        print("\n" + "="*40)
        print("          📊 DEM 数据体检报告")
        print("="*40)
        print(f"📁 文件名称: {os.path.basename(path)}")
        print(f"📐 数据形状 (Shape): {data.shape}")
        print(f"🗄️ 数据类型 (Dtype): {data.dtype}")
        print("-" * 40)
        print(f"⬇️ 最小值 (Min): {data.min()}")
        print(f"⬆️ 最大值 (Max): {data.max()}")
        print(f"🟰 平均值 (Mean): {data.mean():.2f}")
        print("="*40)
        
        # 智能诊断
        max_val = data.max()
        if max_val > 20000:
            print("\n💡 诊断建议：")
            print("你的最大值非常大（超过两万）。这说明你的数据大概率和 VAE 训练时（最高62789）是同一套量纲。")
            print("你可以安心使用原来的 norm_params.json！")
        elif max_val == 255 and data.dtype == np.uint8:
             print("\n⚠️ 诊断建议：")
             print("你的图片是 8-bit 的普通灰度图（最大值 255）。这完全丢失了真实的高程信息！")
             print("请确认你下载的原始数据是不是这种格式。如果是，请重新下载 16-bit 的 DEM。")
        elif max_val < 10000:
            print("\n⚠️ 诊断建议：")
            print("你的最大值比较小（只有几百或几千），这大概率是真实的【海拔米数】。")
            print("这和 VAE 认知的 62789 严重不符！如果你继续用旧的 json，高程会被严重压扁。")
            print("如果出现这种情况，你需要重新统计 VAE 数据的极值！")

    except Exception as e:
        print(f"❌ 读取失败: {e}")

if __name__ == "__main__":
    check_image_data(image_path)