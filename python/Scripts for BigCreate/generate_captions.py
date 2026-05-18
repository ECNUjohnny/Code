"""
地形双模态自动打标脚本 (Auto-Captioning)
将成对的高度图和卫星纹理图发给视觉大模型，生成高质量的 Text Prompt。
"""

import os
import base64
import json
from pathlib import Path
from tqdm import tqdm
from openai import OpenAI

# ==========================================
# 1. 配置区域 (请根据你的实际情况修改)
# ==========================================
# 你的 API Key 和 Base URL (如果是官方 OpenAI 则不用填 BASE_URL)
# 如果你用国内的中转 API 或阿里云通义千问等兼容接口，请替换为对应的 URL
API_KEY = "sk-你的API_KEY"
BASE_URL = "https://api.openai.com/v1" # 例如 Qwen 是 "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME = "gpt-4o" # 或者 "qwen-vl-max" 等支持视觉的模型

# 数据路径设定
DEM_DIR = "./data/origin/heightmaps"    # 高度图所在目录
RGB_DIR = "./data/origin/satellite"     # 卫星图所在目录
OUTPUT_FILE = "./data/process/captions.jsonl" # 输出文件 (JSON Lines 格式，方便断点续传)

# 假设高度图和卫星图文件名完全一致，例如： terrain_001.png
# 如果前后缀不同，可以在下方的匹配逻辑里修改

# ==========================================
# 2. 核心 Prompt 引擎 (极其重要：决定了你 U-Net 的学习质量)
# ==========================================
SYSTEM_PROMPT = """
你是一位顶级的地质学家和地理信息系统（GIS）专家。
我现在会给你两张对齐的地形图像：
第一张是 DEM 高度图（灰度图，越亮代表海拔越高）。
第二张是 RGB 卫星纹理图（展示真实地表覆盖和颜色）。

请仔细观察两张图的空间对应关系，并用一段简洁、专业的英文（不超过 50 个单词）描述该地貌。
你的描述必须包含以下三个维度的信息：
1. 宏观地貌类型（如峡谷、平原、火山、丹霞、丘陵、山脉等）。
2. 高度图呈现的几何特征（如陡峭的悬崖、平缓的坡度、深邃的沟壑等）。
3. 卫星图呈现的表面纹理与颜色（如红色的砂岩、绿色的植被覆盖、干旱的裸露岩石等）。

示例输出格式：
"A top-down aerial view of a Danxia landform, featuring deep narrow canyons with steep vertical cliffs visible in the heightmap, covered by prominent red sandstone textures and sparse green vegetation in the satellite imagery."

直接输出英文描述，不要包含任何多余的解释、寒暄或 Markdown 格式。
"""

# ==========================================
# 3. 工具函数
# ==========================================
def encode_image_to_base64(image_path: str) -> str:
    """将图片文件转换为 Base64 编码的字符串"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_existing_processed_files(output_file: str) -> set:
    """读取已处理的文件列表，用于断点续传"""
    processed = set()
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    processed.add(data["filename"])
                except:
                    pass
    return processed

# ==========================================
# 4. 主执行逻辑
# ==========================================
def main():
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    
    # 获取所有 DEM 文件
    dem_files = [f for f in os.listdir(DEM_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))]
    processed_files = get_existing_processed_files(OUTPUT_FILE)
    
    # 过滤掉已经处理过的文件
    files_to_process = [f for f in dem_files if f not in processed_files]
    print(f"总计找到 {len(dem_files)} 个文件。")
    print(f"已跳过 {len(processed_files)} 个，还需处理 {len(files_to_process)} 个。")
    
    if len(files_to_process) == 0:
        print("所有图片均已打标完成！")
        return

    # 打开文件句柄准备追加写入
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as out_f:
        pbar = tqdm(files_to_process, desc="请求大模型 API 打标中")
        
        for filename in pbar:
            dem_path = os.path.join(DEM_DIR, filename)
            rgb_path = os.path.join(RGB_DIR, filename) # 假设同名
            
            if not os.path.exists(rgb_path):
                tqdm.write(f"⚠️ 警告: 找不到对应的卫星图 {rgb_path}，跳过此文件。")
                continue
                
            try:
                base64_dem = encode_image_to_base64(dem_path)
                base64_rgb = encode_image_to_base64(rgb_path)
                
                # 组装发给大模型的 payload
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        },
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "第一张图是高度图，第二张图是对应的卫星图。请描述："},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_dem}"}},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_rgb}"}}
                            ]
                        }
                    ],
                    max_tokens=100, # 描述不需要太长，省钱省时间
                    temperature=0.3 # 降低随机性，保证描述的客观准确
                )
                
                # 提取模型生成的文本
                caption = response.choices[0].message.content.strip()
                
                # 保存结果
                result_dict = {
                    "filename": filename,
                    "prompt": caption
                }
                out_f.write(json.dumps(result_dict, ensure_ascii=False) + '\n')
                out_f.flush() # 强制立刻写入硬盘，防止中途断电丢失
                
                # 在进度条上顺便展示一下刚生成的 prompt
                pbar.set_postfix({"Latest": caption[:20] + "..."})
                
            except Exception as e:
                tqdm.write(f"❌ 处理文件 {filename} 时发生网络或 API 错误: {e}")
                # 发生错误不停机，继续尝试下一个

if __name__ == "__main__":
    main()