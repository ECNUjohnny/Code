import requests
import os
import time
import rasterio
from rasterio.enums import Resampling
from rasterio.windows import Window
import numpy as np

# ================= 1. 基础配置区 =================
# 填入你的 OpenTopography API Key
API_KEY = "b21b7d8e4a0c90d358df7360822b6e76" 

# 定义你要保存的特定文件夹路径 (Windows 路径建议前面加 r，或者使用双斜杠 \\)
# 例如: r"D:\Unity_Projects\GIS_Data\DEMs"
SAVE_FOLDER = r"D:/File/Research/Dataset/Opentopography" 

# 确保保存的文件夹存在，如果不存在则自动创建
os.makedirs(SAVE_FOLDER, exist_ok=True)

# ================= 2. 目标数据区 =================
# 将你需要下载的多个区域写成一个列表
# bounds 的顺序务必保持为: (south, north, west, east) 即 (南纬, 北纬, 西经, 东经)
target_areas = [
    # ========== 亚洲 (Asia) ==========
    {
        "name": "Yarlung_Tsangpo_Grand_Canyon", # 雅鲁藏布大峡谷 (中国西藏) - 世界最深最长的峡谷之一
        "bounds": (29.400, 30.100, 94.700, 95.600)
    },
    {
        "name": "Tiger_Leaping_Gorge", # 虎跳峡 (中国云南)
        "bounds": (27.200, 27.400, 100.050, 100.250)
    },
    {
        "name": "Kali_Gandaki_Gorge", # 卡利甘达基峡谷 (尼泊尔) - 喜马拉雅山脉中的极深峡谷
        "bounds": (28.500, 28.850, 83.550, 83.850)
    },
    
    # ========== 非洲 (Africa) - 东非大裂谷带 ==========
    {
        "name": "Great_Rift_Valley_Ethiopia", # 东非大裂谷 (埃塞俄比亚段)
        "bounds": (7.000, 10.000, 38.500, 40.500)
    },
    {
        "name": "Great_Rift_Valley_Kenya", # 东非大裂谷 (肯尼亚格雷戈里裂谷段)
        "bounds": (-2.500, 1.500, 35.500, 36.500)
    },
    {
        "name": "Great_Rift_Valley_Albertine", # 东非大裂谷 (西线阿尔伯特裂谷，坦噶尼喀湖周边)
        "bounds": (-8.000, -3.000, 29.000, 31.000)
    },
    {
        "name": "Fish_River_Canyon", # 鱼河大峡谷 (纳米比亚) - 非洲最大峡谷
        "bounds": (-28.000, -27.500, 17.500, 17.850)
    },
    {
        "name": "Blyde_River_Canyon", # 布莱德河峡谷 (南非)
        "bounds": (-24.650, -24.500, 30.750, 30.900)
    }
]

print(f"初始化完成，准备将 {len(target_areas)} 个高程图下载至目录: {SAVE_FOLDER}\n")

# ================= 3. 循环下载区 =================
for i, area in enumerate(target_areas, 1):
    name = area["name"]
    south, north, west, east = area["bounds"]
    
    print(f"[{i}/{len(target_areas)}] 正在向云端请求: {name} ...")
    
    # 构造请求 URL
    url = f"https://portal.opentopography.org/API/globaldem?demtype=NASADEM&south={south}&north={north}&west={west}&east={east}&outputFormat=GTiff&API_Key={API_KEY}"
    
    # 将文件夹路径和具体的文件名拼接起来
    file_path = os.path.join(SAVE_FOLDER, f"{name}.tif")
    
    try:
        # 发送请求
        response = requests.get(url)
        
        if response.status_code == 200:
            # 成功！写入指定路径的文件
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"  -> 下载成功！已保存至: {file_path}")
        else:
            print(f"  -> 出错啦: 状态码 {response.status_code}, 错误信息: {response.text}")
            
    except Exception as e:
        print(f"  -> 网络请求发生异常: {e}")
        
    # ⚠️ 极其关键的一步：休眠防封禁！
    # 每次下载完停顿 2-3 秒，做个文明的爬虫。
    time.sleep(3) 

print("\n所有下载任务已处理完毕！")