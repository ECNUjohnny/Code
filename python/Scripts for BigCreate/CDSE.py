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
    # ================= 1. 中国 - 极致的高大沙山与复合沙丘 =================
    {
        # 巴丹吉林沙漠核心区 (Badain Jaran Desert) - 拥有世界上最高的静止沙丘（必鲁图峰），沙山与湖泊相间分布，高程起伏惊人
        "name": "Badain_Jaran_Mega_Dunes_InnerMongolia",
        "bounds": (39.500, 40.100, 102.000, 102.800) # lat_diff: 0.60, lon_diff: 0.80
    },
    {
        # 塔克拉玛干沙漠腹地 (Taklamakan Desert) - 世界第二大流动沙漠，密集的复合型新月形沙丘链和巨大的沙垄
        "name": "Taklamakan_Barchan_Dunes_Xinjiang",
        "bounds": (38.700, 39.300, 82.700, 83.500) # lat_diff: 0.60, lon_diff: 0.80
    },
    {
        # 库木塔格沙漠 (Kumtag Desert) - 典型的羽毛状沙丘，风沙地貌的“活化石”，沙垄排列极具几何规律
        "name": "Kumtag_Feather_Dunes_Xinjiang",
        "bounds": (42.400, 43.000, 90.000, 90.800) # lat_diff: 0.60, lon_diff: 0.80
    },

    # ================= 2. 中东 - 浩瀚的流动沙海 =================
    {
        # 鲁卜哈利沙漠 / 空旷四分之一 (Rub' al Khali, Saudi Arabia/UAE) - 世界上最大的连续沙海，包含极其壮观的巨型线状和星状复合沙丘
        "name": "Empty_Quarter_Star_Dunes_Arabia",
        "bounds": (19.700, 20.300, 52.600, 53.400) # lat_diff: 0.60, lon_diff: 0.80
    },
    {
        # 伊朗卡维尔盐漠 (Dasht-e Kavir, Iran) - 巨大的干涸盐沼，地表呈现出如同大脑褶皱般的复杂盐壳多边形纹理（需极高精度DEM展现，30m可见宏观波纹）
        "name": "Dasht_e_Kavir_Salt_Desert_Iran",
        "bounds": (34.300, 34.900, 54.400, 55.200) # lat_diff: 0.60, lon_diff: 0.80
    },

    # ================= 3. 非洲 - 撒哈拉与纳米布 =================
    {
        # 纳米布沙漠苏丝斯黎 (Sossusvlei, Namib Desert, Namibia) - 世界上最古老的沙漠，以极其高大且边缘锐利的红色星状沙丘闻名
        "name": "Namib_Sossusvlei_Red_Dunes_Namibia",
        "bounds": (-25.000, -24.400, 15.000, 15.700) # lat_diff: 0.60, lon_diff: 0.70
    },
    {
        # 撒哈拉大东方沙海 (Grand Erg Oriental, Algeria) - 撒哈拉沙漠中极其广阔的沙海，呈现出连绵不绝的密集圆顶和新月沙丘
        "name": "Sahara_Grand_Erg_Oriental_Algeria",
        "bounds": (29.700, 30.300, 6.600, 7.400) # lat_diff: 0.60, lon_diff: 0.80
    },
    {
        # 埃及理查特结构周边 (Richat Structure edge, Mauritania) - 撒哈拉之眼的边缘地带，沙哈拉岩石荒漠与流沙交界处
        "name": "Sahara_Rocky_Desert_Mauritania",
        "bounds": (20.800, 21.400, -11.800, -11.000) # lat_diff: 0.60, lon_diff: 0.80
    },

    # ================= 4. 澳洲与美洲 - 平行沙垄与极旱荒漠 =================
    {
        # 澳大利亚辛普森沙漠 (Simpson Desert, Australia) - 全球最大的平行沙垄沙漠，数百条笔直的红色沙垄连绵上百公里
        "name": "Simpson_Parallel_Dunes_Australia",
        "bounds": (-24.300, -23.700, 136.600, 137.400) # lat_diff: 0.60, lon_diff: 0.80
    },
    {
        # 智利阿塔卡马沙漠核心区 (Atacama Desert, Chile) - 地球上最干旱的非极地沙漠，类似火星地表，充满干盐湖、砾漠与风化山体
        "name": "Atacama_Hyperarid_Desert_Chile",
        "bounds": (-24.300, -23.700, -68.900, -68.100) # lat_diff: 0.60, lon_diff: 0.80
    },
    {
        # 美国死谷国家公园 (Death Valley, USA) - 北美最低点，包含恶水盆地的广阔盐滩、冲积扇以及麦斯奎特平原的沙丘系统
        "name": "Death_Valley_Basin_USA",
        "bounds": (36.100, 36.700, -117.200, -116.400) # lat_diff: 0.60, lon_diff: 0.80
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