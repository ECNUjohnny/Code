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
SAVE_FOLDER = r"D:/File/Research/Dataset/opentopography" 

# 确保保存的文件夹存在，如果不存在则自动创建
os.makedirs(SAVE_FOLDER, exist_ok=True)

# ================= 2. 目标数据区 =================
# 将你需要下载的多个区域写成一个列表
# bounds 的顺序务必保持为: (south, north, west, east) 即 (南纬, 北纬, 西经, 东经)
target_areas = [
    # 敦煌雅丹（甘肃）
    {
        "name": "Dunhuang_Main",
        "bounds": (40.450, 40.550, 92.950, 93.100)
    },
    {
        "name": "Dunhuang_North",
        "bounds": (40.550, 40.650, 92.980, 93.150)
    },
    {
        "name": "Dunhuang_South",
        "bounds": (40.350, 40.450, 92.900, 93.000)
    },

    # 柴达木盆地雅丹群（青海）
    {
        "name": "Qaidam_Wusute_Water_Yardang", # 水上雅丹
        "bounds": (37.780, 37.850, 92.200, 92.300)
    },
    {
        "name": "Qaidam_Nanbaxian", # 南八仙
        "bounds": (38.150, 38.250, 93.350, 93.450)
    },
    {
        "name": "Qaidam_Eboliang", # 俄博梁
        "bounds": (38.550, 38.650, 92.250, 92.350)
    },
    {
        "name": "Qaidam_Mangya", # 茫崖周边
        "bounds": (38.300, 38.400, 91.500, 91.650)
    },
    {
        "name": "Qaidam_Lenghu", # 冷湖周边
        "bounds": (38.700, 38.800, 92.800, 92.950)
    },

    # 哈密魔鬼城（新疆）
    {
        "name": "Hami_Wubao", # 五堡
        "bounds": (42.680, 42.780, 92.750, 92.900)
    },
    {
        "name": "Hami_Sandaoling", # 三道岭
        "bounds": (42.850, 42.950, 92.500, 92.650)
    },
    {
        "name": "Hami_Shiqiang", # 十八里房/石城子附近
        "bounds": (42.500, 42.600, 93.000, 93.150)
    },

    # 乌尔禾魔鬼城（新疆克拉玛依）
    {
        "name": "Wuerhe_Main",
        "bounds": (46.080, 46.150, 85.280, 85.350)
    },
    {
        "name": "Wuerhe_East",
        "bounds": (46.100, 46.180, 85.350, 85.450)
    },
    {
        "name": "Wuerhe_South",
        "bounds": (46.000, 46.080, 85.200, 85.300)
    },

    # 罗布泊雅丹群（新疆）
    {
        "name": "LopNur_Bailongdui", # 白龙堆
        "bounds": (40.400, 40.500, 90.500, 90.700)
    },
    {
        "name": "LopNur_Sanlongsha", # 三垄沙
        "bounds": (40.100, 40.250, 90.800, 90.950)
    },
    {
        "name": "LopNur_Longcheng", # 龙城
        "bounds": (40.600, 40.750, 90.200, 90.350)
    },

    # 吐鲁番及周边雅丹（新疆）
    {
        "name": "Turpan_Toksun", # 托克逊盘吉尔
        "bounds": (42.650, 42.750, 88.500, 88.650)
    },
    {
        "name": "Turpan_Shanshan", # 鄯善周边
        "bounds": (42.700, 42.800, 89.900, 90.050)
    },

    # 库车雅丹（新疆）
    {
        "name": "Kuche_Yardang", # 库车周边
        "bounds": (41.650, 41.750, 83.050, 83.150)
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