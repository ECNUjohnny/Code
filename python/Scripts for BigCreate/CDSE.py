import os
import requests
import time
import math
from dotenv import load_dotenv
from urllib3.exceptions import ProtocolError 

# ================= 1. 环境与路径配置 =================
load_dotenv()
CLIENT_ID = os.getenv("CDSE_CLIENT_ID")
CLIENT_SECRET = os.getenv("CDSE_CLIENT_SECRET")

# 设置并创建两个独立的输出文件夹
RGB_DIR = "D:/WorkSpace/Research/dataset/RGB from CDSE"
DEM_DIR = "D:/WorkSpace/Research/dataset/DEM from CDSE"
os.makedirs(RGB_DIR, exist_ok=True)
os.makedirs(DEM_DIR, exist_ok=True)

# CDSE API 端点
TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
PROCESS_URL = "https://sh.dataspace.copernicus.eu/api/v1/process"

# ================= 2. 定义批量下载的区域数组 =================
# 包含 50 个高山和复杂地形的列表
input_regions = [
    # ================= 联合国教科文组织“中国丹霞”世界自然遗产 =================
    {
        "name": "Danxia_Mountain_Guangdong",
        "bounds": (24.885, 25.165, 113.570, 113.880)
    },
    {
        "name": "Wuyi_Mountain_Fujian",
        "bounds": (27.510, 27.790, 117.795, 118.105)
    },
    {
        "name": "Longhu_Mountain_Jiangxi",
        "bounds": (27.940, 28.220, 116.815, 117.125)
    },
    {
        "name": "Langshan_Mountain_Hunan",
        "bounds": (26.210, 26.490, 110.695, 111.005)
    },
    {
        "name": "Chishui_Danxia_Guizhou",
        "bounds": (28.310, 28.590, 105.845, 106.155)
    },
    {
        "name": "Taining_Danxia_Fujian",
        "bounds": (26.730, 27.010, 116.945, 117.255)
    },
    {
        "name": "Jianglang_Mountain_Zhejiang",
        "bounds": (28.390, 28.670, 118.405, 118.715)
    },

    # ================= 中国西北干旱/高原型 著名丹霞 =================
    {
        # 纬度升高，经度补偿跨度增加至 0.34°
        "name": "Zhangye_Danxia_Gansu",
        "bounds": (38.810, 39.090, 99.980, 100.320)
    },
    {
        "name": "Binggou_Danxia_Gansu",
        "bounds": (38.790, 39.070, 99.700, 100.040)
    },
    {
        # 纬度最高，经度补偿跨度增加至 0.37°
        "name": "Kuqa_Grand_Canyon_Xinjiang",
        "bounds": (42.030, 42.310, 82.960, 83.330)
    },
    {
        "name": "Kanbula_Danxia_Qinghai",
        "bounds": (35.980, 36.260, 101.130, 101.470)
    },
    {
        "name": "Jingbian_Wave_Valley_Shaanxi",
        "bounds": (37.420, 37.700, 108.590, 108.930)
    },

    # ================= 其他具有独特地貌特征的中国丹霞区域 =================
    {
        "name": "Gaoyiling_Chenzhou_Hunan",
        "bounds": (25.770, 26.050, 112.965, 113.275)
    },
    {
        "name": "Jianmen_Pass_Sichuan",
        "bounds": (32.080, 32.360, 105.390, 105.730)
    },
    {
        "name": "Qiyun_Mountain_Anhui",
        "bounds": (29.670, 29.950, 117.865, 118.175)
    },

    # ================= 北美洲：红岩峡谷与孤峰巨怪 =================
    {
        "name": "Zion_National_Park_USA",
        "bounds": (37.130, 37.410, -113.140, -112.800)
    },
    {
        "name": "Monument_Valley_USA",
        "bounds": (36.850, 37.130, -110.260, -109.920)
    },
    {
        "name": "Sedona_Red_Rocks_USA",
        "bounds": (34.730, 35.010, -111.940, -111.600)
    },

    # ================= 南美洲：干旱区巨型红壁 =================
    {
        "name": "Talampaya_National_Park_Argentina",
        "bounds": (-29.910, -29.630, -67.985, -67.675) 
    },

    # ================= 澳洲：古老大陆的红层奇观 =================
    {
        "name": "Kata_Tjuta_Australia",
        "bounds": (-25.440, -25.160, 130.565, 130.875)
    },
    {
        # 纬度极低，经度补偿跨度缩小至 0.29°
        "name": "Purnululu_National_Park_Australia",
        "bounds": (-17.560, -17.280, 128.175, 128.465)
    },

    # ================= 中东/非洲：沙漠里的红色群山 =================
    {
        "name": "Wadi_Rum_Jordan",
        "bounds": (29.430, 29.710, 35.265, 35.575)
    }
]

# ================= 3. 定义云端微代码 (Evalscripts) =================
# 💡 改进版 RGB 光学卫星代码：使用 Gamma 矫正应对冰雪高反照率
EVALSCRIPT_RGB = """
//VERSION=3
function setup() {
    return {
        input: ["B04", "B03", "B02", "dataMask"],
        output: { bands: 3 } 
    };
}

function evaluatePixel(sample) {
    // 设置 Gamma 值 (大于 1.0 可以提亮暗部，同时平滑压制高亮部分)
    // 1.5 到 2.0 之间适合冰川/雪山等高反照率地貌
    let gamma = 1.6; 
    let gain = 1.2; // 整体亮度微调系数
    
    // 应用 Gamma 矫正公式: Out = Gain * (In ^ (1/Gamma))
    let r = gain * Math.pow(sample.B04, 1/gamma);
    let g = gain * Math.pow(sample.B03, 1/gamma);
    let b = gain * Math.pow(sample.B02, 1/gamma);
    
    return [r, g, b];
}
"""

# DEM 高程代码 (要求返回 32位 真实海拔浮点数)
EVALSCRIPT_DEM = """
//VERSION=3
function setup() {
    return {
        input: ["DEM"],
        output: { bands: 1, sampleType: "FLOAT32" }
    };
}
function evaluatePixel(sample) {
    return [sample.DEM];
}
"""

# ================= 4. 核心下载函数 =================
def fetch_token():
    """获取 API 访问令牌 (使用安全的 client_credentials 模式)"""
    resp = requests.post(TOKEN_URL, data={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })
    resp.raise_for_status()
    return resp.json()["access_token"]

def calculate_unified_size(bbox):
    """统一计算区域的最佳像素尺寸：以30米为基准，寻找最接近的 2 的指数"""
    west, south, east, north = bbox
    delta_lat = north - south
    distance_meters = delta_lat * 111000
    true_pixels = distance_meters / 30.0
    power = round(math.log2(true_pixels))
    power = max(8, min(11, power))
    target_size = 2 ** power
    return target_size

def download_data(name, bbox, current_token, data_type, target_size):
    """下载引擎：带有 Token 自动刷新和网络重试机制"""
    
    payload = {
        "input": {
            "bounds": {
                "bbox": bbox,
                "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"}
            },
            "data": []
        },
        "output": {
            "width": target_size,
            "height": target_size,
            "responses": [{"identifier": "default", "format": {"type": "image/tiff"}}]
        }
    }

    if data_type == "RGB":
        payload["input"]["data"] = [{
            "type": "sentinel-2-l2a",
            "dataFilter": {
                "timeRange": {"from": "2021-01-01T00:00:00Z", "to": "2025-12-31T23:59:59Z"},
                "maxCloudCoverage": 5
            }
        }]
        payload["evalscript"] = EVALSCRIPT_RGB
        out_path = os.path.join(RGB_DIR, f"{name}_RGB.tif")
        
    elif data_type == "DEM":
        payload["input"]["data"] = [{"type": "dem"}]
        payload["evalscript"] = EVALSCRIPT_DEM
        out_path = os.path.join(DEM_DIR, f"{name}_DEM.tif")

    if os.path.exists(out_path):
        print(f"  -> {data_type} 已存在，跳过。")
        return current_token 

    max_retries = 3
    
    for attempt in range(max_retries):
        headers = {"Authorization": f"Bearer {current_token}", "Accept": "image/tiff"}
        
        try:
            resp = requests.post(PROCESS_URL, headers=headers, json=payload, timeout=(15, 120))
            
            if resp.status_code == 401:
                print(f"  ⚠️ Token 已过期 (401)，正在向服务器申请新 Token...")
                current_token = fetch_token()
                continue 
            
            resp.raise_for_status()
            
            with open(out_path, "wb") as f:
                f.write(resp.content)
            print(f"  -> 成功下载 {data_type}: {out_path}")
            
            break 
            
        except (requests.exceptions.RequestException, ProtocolError) as e:
            print(f"  ❌ {data_type} 网络请求中断 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(5) 
            else:
                print(f"  -> 达到最大重试次数，{data_type} 下载失败。")

    return current_token

# ================= 5. 执行主循环 =================
if __name__ == "__main__":
    global_token = fetch_token()
    print(f"\n✅ 成功获取初始 Token！准备批量处理 {len(input_regions)} 个地貌区域...\n")
    
    for idx, region in enumerate(input_regions, 1):
        name = region["name"]
        south, north, west, east = region["bounds"]
        
        bbox_cdse = [west, south, east, north]
        unified_size = calculate_unified_size(bbox_cdse)
        
        print(f"\n[{idx}/{len(input_regions)}] 正在处理: {name}")
        print(f"  -> 已计算统一网格分辨率: {unified_size} x {unified_size}")
        
        global_token = download_data(name, bbox_cdse, global_token, "DEM", unified_size)
        global_token = download_data(name, bbox_cdse, global_token, "RGB", unified_size)
        
        time.sleep(1)
        
    print("\n🎉 全部数据批处理下载完成！")