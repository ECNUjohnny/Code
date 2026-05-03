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
RGB_DIR = "D:/WorkSpace/Research/dataset/DEM from CDSE"
DEM_DIR = "D:/WorkSpace/Research/dataset/RGB from CDSE"
os.makedirs(RGB_DIR, exist_ok=True)
os.makedirs(DEM_DIR, exist_ok=True)

# CDSE API 端点
TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
PROCESS_URL = "https://sh.dataspace.copernicus.eu/api/v1/process"

# ================= 2. 定义批量下载的区域数组 =================
# 包含 50 个高山和复杂地形的列表
input_regions = [
    # ========== 亚洲 (Asia) ==========
    {
        "name": "Mount_Everest_Himalayas",
        "bounds": (27.888, 28.088, 86.825, 87.025)
    },
    {
        "name": "K2_Karakoram",
        "bounds": (35.781, 35.981, 76.413, 76.613)
    },
    {
        "name": "Annapurna_Massif",
        "bounds": (28.496, 28.696, 83.720, 83.920)
    },
    {
        "name": "Mount_Kinabalu",
        "bounds": (5.975, 6.175, 116.458, 116.658)
    },
    {
        "name": "Mount_Damavand",
        "bounds": (35.851, 36.051, 52.012, 52.212)
    },
    {
        "name": "Mount_Ararat",
        "bounds": (39.602, 39.802, 44.199, 44.399)
    },
    {
        "name": "Mount_Siguniang",
        "bounds": (31.006, 31.206, 102.802, 103.002)
    },
    {
        "name": "Namcha_Barwa",
        "bounds": (29.529, 29.729, 94.954, 95.154)
    },
    {
        "name": "Tomur_Peak",
        "bounds": (41.938, 42.138, 80.029, 80.229)
    },
    {
        "name": "Tirich_Mir",
        "bounds": (36.154, 36.354, 71.741, 71.941)
    },
    {
        "name": "Bogda_Peak",
        "bounds": (43.697, 43.897, 88.433, 88.633)
    },
    {
        "name": "Nanga_Parbat",
        "bounds": (35.137, 35.337, 74.489, 74.689)
    },
    {
        "name": "Minya_Konka",
        "bounds": (29.495, 29.695, 101.778, 101.978)
    },
    {
        "name": "Mount_Apo",
        "bounds": (6.887, 7.087, 125.171, 125.371)
    },
    {
        "name": "Belukha_Mountain",
        "bounds": (49.706, 49.906, 86.488, 86.688)
    },

    # ========== 欧洲 (Europe) ==========
    {
        "name": "Matterhorn",
        "bounds": (45.876, 46.076, 7.558, 7.758)
    },
    {
        "name": "Mont_Blanc_Massif",
        "bounds": (45.732, 45.932, 6.765, 6.965)
    },
    {
        "name": "Grossglockner",
        "bounds": (46.974, 47.174, 12.593, 12.793)
    },
    {
        "name": "Pico_de_Aneto",
        "bounds": (42.532, 42.732, 0.557, 0.757)
    },
    {
        "name": "Mount_Elbrus",
        "bounds": (43.249, 43.449, 42.338, 42.538)
    },
    {
        "name": "Mount_Triglav",
        "bounds": (46.278, 46.478, 13.740, 13.940)
    },
    {
        "name": "Galdhopiggen",
        "bounds": (61.536, 61.736, 8.212, 8.412)
    },
    {
        "name": "Kebnekaise",
        "bounds": (67.802, 68.002, 18.416, 18.616)
    },
    {
        "name": "Gran_Paradiso",
        "bounds": (45.419, 45.619, 7.166, 7.366)
    },
    {
        "name": "Gerlachovsky_Stit",
        "bounds": (49.064, 49.264, 20.033, 20.233)
    },

    # ========== 北美洲 (North America) ==========
    {
        "name": "Denali_Massif",
        "bounds": (62.969, 63.169, -151.107, -150.907)
    },
    {
        "name": "Mount_Rainier",
        "bounds": (46.752, 46.952, -121.860, -121.660)
    },
    {
        "name": "Mount_Whitney",
        "bounds": (36.478, 36.678, -118.392, -118.192)
    },
    {
        "name": "Mount_Logan",
        "bounds": (60.467, 60.667, -140.505, -140.305)
    },
    {
        "name": "Pico_de_Orizaba",
        "bounds": (18.930, 19.130, -97.369, -97.169)
    },
    {
        "name": "Grand_Teton",
        "bounds": (43.641, 43.841, -110.902, -110.702)
    },
    {
        "name": "Mount_Robson",
        "bounds": (53.010, 53.210, -119.256, -119.056)
    },
    {
        "name": "Yosemite_Half_Dome",
        "bounds": (37.646, 37.846, -119.633, -119.433)
    },
    {
        "name": "Mount_Shasta",
        "bounds": (41.309, 41.509, -122.294, -122.094)
    },
    {
        "name": "Popocatepetl",
        "bounds": (18.922, 19.122, -98.727, -98.527)
    },

    # ========== 南美洲 (South America) ==========
    {
        "name": "Aconcagua",
        "bounds": (-32.753, -32.553, -70.110, -69.910)
    },
    {
        "name": "Huascaran",
        "bounds": (-9.214, -9.014, -77.705, -77.505)
    },
    {
        "name": "Fitz_Roy",
        "bounds": (-49.371, -49.171, -73.143, -72.943)
    },
    {
        "name": "Chimborazo",
        "bounds": (-1.569, -1.369, -78.916, -78.716)
    },
    {
        "name": "Cotopaxi",
        "bounds": (-0.780, -0.580, -78.537, -78.337)
    },
    {
        "name": "Mount_Roraima",
        "bounds": (5.115, 5.315, -60.833, -60.633)
    },
    {
        "name": "Illimani",
        "bounds": (-16.735, -16.535, -67.884, -67.684)
    },
    {
        "name": "Torres_del_Paine_Cuernos",
        "bounds": (-51.083, -50.883, -73.066, -72.866)
    },

    # ========== 非洲 (Africa) ==========
    {
        "name": "Mount_Kilimanjaro_Kibo",
        "bounds": (-3.167, -2.967, 37.255, 37.455)
    },
    {
        "name": "Mount_Kenya_Batian",
        "bounds": (-0.250, -0.050, 37.208, 37.408)
    },
    {
        "name": "Rwenzori_Mount_Stanley",
        "bounds": (0.286, 0.486, 29.772, 29.972)
    },
    {
        "name": "Mount_Toubkal",
        "bounds": (30.963, 31.163, -8.015, -7.815)
    },

    # ========== 大洋洲与南极洲 (Oceania & Antarctica) ==========
    {
        "name": "Aoraki_Mount_Cook",
        "bounds": (-43.695, -43.495, 170.041, 170.241)
    },
    {
        "name": "Puncak_Jaya",
        "bounds": (-4.183, -3.983, 137.083, 137.283)
    },
    {
        "name": "Mount_Vinson",
        "bounds": (-78.625, -78.425, -85.717, -85.517)
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