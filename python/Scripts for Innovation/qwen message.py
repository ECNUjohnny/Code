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


client = OpenAI(api_key=API_KEY, base_url=BASE_URL)



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
           # 设置极简 Prompt
            sys_msg = "You are an expert geologist and geographic terrain analyst acting as a strict JSON API. Output ONLY valid JSON."
            usr_msg = (
            )
            
            

if __name__ == "__main__":
    print("Initializing Auto-Annotation Pipeline...")
    print("Pipeline Finished.")