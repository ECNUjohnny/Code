import json
import base64
import io
import cv2
import numpy as np
from pathlib import Path
from PIL import Image
from tqdm import tqdm
from openai import OpenAI
import re

cv2.utils.logging.setLogLevel(cv2.utils.logging.LOG_LEVEL_SILENT)

# ==========================================
# 1. 基础配置
# ==========================================
API_KEY = "sk-local-test" 
BASE_URL = "http://127.0.0.1:8000/v1" 
MODEL_NAME = "qwen-vl" 

# 请修改为你实际的 dataset 根目录
BASE_DIR = Path(r"E:\WorkSpace\Data\unet_test")
RGB_DIR = BASE_DIR / "rgb"
DEM_DIR = BASE_DIR / "dem"
TXT_DIR = BASE_DIR / "txt"

# 自动创建 txt 输出文件夹
TXT_DIR.mkdir(parents=True, exist_ok=True)

DANXIA = r"E:\WorkSpace\Data\dataset\Danxia\outputs"
KARST = r"E:\WorkSpace\Data\dataset\Karst\Karst"
LOESS = r"E:\WorkSpace\Data\dataset\Huangtu\Huangtu"
ICE = r"E:\WorkSpace\Data\dataset\IceMountain\IceMountain"
DESERT = r"E:\WorkSpace\Data\dataset\desert\desert"
YARDANG = r"E:\WorkSpace\Data\dataset\Yadan\Yadan"
INPUT = r"E:\WorkSpace\Data\unet\txt"

danxia = set()
karst = set()
loess = set()
ice = set()
desert = set()
yardang = set()

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def extract_name(terrain_set: set, dir_path: str):
    path = Path(dir_path)

    dirs = [d for d in path.iterdir() if d.is_dir()]

    for dir in tqdm(dirs, desc='name', ncols=100):
        terrain_set.add(dir.name)


def init():
    extract_name(danxia, DANXIA)
    extract_name(karst, KARST)
    extract_name(ice, ICE)
    extract_name(desert, DESERT)
    extract_name(yardang, YARDANG)
    extract_name(loess, LOESS)

# ==========================================
# 2. 图像解码与转换模块
# ==========================================
def encode_img(path: Path) -> str:
    # 使用纯字符串转换，防止 OpenCV 对 Path 对象报错
    img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Failed to read: {path}")

    # 判断是 3 通道 (RGB) 还是单通道 (DEM)
    if len(img.shape) == 3: 
        # OpenCV 默认读取彩色图为 BGR，必须转回 RGB，否则大模型会看错颜色
        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        elif img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        img_8 = img.astype(np.uint8)
    else: 
        # DEM 相对值转换逻辑
        if img.dtype == np.uint16:
            img_8 = (img / 256.0).clip(0, 255).astype(np.uint8)
        elif img.dtype in [np.float16, np.float32, np.float64]:
            img_8 = (img * 255.0).clip(0, 255).astype(np.uint8)
        else:
            img_8 = img.astype(np.uint8)
    
    pil_img = Image.fromarray(img_8)
    if pil_img.mode != 'RGB':
        pil_img = pil_img.convert('RGB')
    
    buf = io.BytesIO()
    pil_img.save(buf, format="JPEG")
    b64_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    return f"data:image/jpeg;base64,{b64_str}"

# ==========================================
# 3. 核心流水线
# ==========================================
def process_dataset():
    # 抓取所有 rgb 目录下的图片
    rgb_files = [f for f in RGB_DIR.iterdir() if f.suffix.lower() in ['.png', '.tif', '.jpg']]

    cnt = 0

    init()

    # 使用 ncols 锁死进度条宽度，防止终端瀑布流
    for rgb_file in tqdm(rgb_files, desc="Annotating", ncols=100, mininterval=0.5):
        name = rgb_file.stem
        txt_file = TXT_DIR / f"{name}.txt"
        
        # if cnt > 2: break

        cnt += 1

        # 断点续传：如果 txt 已经存在，直接跳过
        if txt_file.exists():
            continue
            
        # 自动匹配同名的 dem 图片（兼容后缀可能不同的情况）
        dem_file = None
        for ext in ['.png', '.tif', '.jpg']:
            temp_path = DEM_DIR / f"{name}{ext}"
            if temp_path.exists():
                dem_file = temp_path
                break
                
        if not dem_file:
            tqdm.write(f"Warning: No matching DEM found for {name}")
            continue
            
        try:
            # 编码两张图片
            b64_rgb = encode_img(rgb_file)
            b64_dem = encode_img(dem_file)
            
            if name in danxia: catagory = "danxia"
            elif name in karst: catagory = "karst"
            elif name in ice: catagory = "ice mountain"
            elif name in desert: catagory = "desert"
            elif name in yardang: catagory = "yardang"
            elif name in loess: catagory = "loess"

            # 设置极简 Prompt
            sys_msg = "You are an expert geologist and geographic terrain analyst acting as a strict JSON API. Output ONLY valid JSON."
            usr_msg = (
                "Image 1 is a DEM (height map). Image 2 is an RGB texture map. "
                f"Hint: This area belongs to {catagory}."
                "As an expert, output a pure JSON object exactly like this template to depict the precise geological and visual features: "
                '{"topology": "...", "erosion": "...", "slope_feel": "...", "surface": "...", "color_palette": "..."}. '
                "For 'color_palette', output ONLY 1 to 3 essential color adjectives (e.g., 'dusty yellow and gray')"
                "Focus exclusively on natural geographical features. Use concise English phrases."
            )
            
            messages = [
                {"role": "system", "content": sys_msg},
                # 伪造用户的第一次提问
                {"role": "user", "content": "Analyze the images and output JSON."},
                # 伪造模型的第一次完美回答（没有一句废话，直接输出 JSON）
                {"role": "assistant", "content": '{\n  "topology": "rolling hills",\n  "erosion": "shallow gullies",\n  "slope_feel": "gentle inclines",\n  "surface": "sparse vegetation"\n}'},
                # 真实的提问开始
                {"role": "user", "content": [
                    {"type": "text", "text": usr_msg},
                    {"type": "image_url", "image_url": {"url": b64_dem}},
                    {"type": "image_url", "image_url": {"url": b64_rgb}}
                ]}
            ]

            # 发送给 Qwen
            resp = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                max_tokens=500,
                temperature=0.15,
                response_format={ "type": "json_object" }
            )
            
            # 清洗思考过程
            ans = resp.choices[0].message.content.strip()
            
            # 终极提取方案：用正则强行挖出 JSON 块
            try:
                # 寻找从第一个 { 开始，到最后一个 } 结束的所有内容 (re.DOTALL 允许跨行匹配)
                match = re.search(r'\{.*\}', ans, re.DOTALL)
                
                if match:
                    json_str = match.group(0)
                    data = json.loads(json_str)
                    
                    # 组装 CLIP 友好的自然语言 (注意 features 改成 is 啦)
                    final_prompt = (
                        f"A view of {data.get('topology', 'terrain')}, "
                        f"characterized by {data.get('erosion', 'erosion')}. "
                        f"The terrain is {data.get('slope_feel', 'slopes')}, "
                        f"featuring a color palette of {data.get('color_palette', 'natural hues')}, " # 
                        f"showing {data.get('surface', 'surface')}."
                    )
                else:
                    raise ValueError("未在回复中找到 JSON 结构")
                    
            except Exception as e:
                # 如果模型彻底发疯连 {} 都没输出，写入一条短警告，防止覆盖大量乱码
                tqdm.write(f"Warning: JSON 解析失败 [{name}] - {e}")
                tqdm.write(f"Original output: {ans[:100]}\n")
                final_prompt = f"A view of terrain, showing natural surface." # 极其安全的保底 Prompt
            
            # 写入对应 txt 文件
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(final_prompt)
                
        except Exception as e:
            # 使用 tqdm.write 打印错误，不会破坏进度条
            tqdm.write(f"Error processing {name}: {e}")

if __name__ == "__main__":
    print("Initializing Auto-Annotation Pipeline...")
    process_dataset()
    print("Pipeline Finished.")