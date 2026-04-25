import os
import requests
import time
import math
from dotenv import load_dotenv

# ================= 1. 环境与路径配置 =================
load_dotenv()
CLIENT_ID = os.getenv("CDSE_CLIENT_ID")
CLIENT_SECRET = os.getenv("CDSE_CLIENT_SECRET")

print(os.getenv("CDSE_CLIENT_ID"))

# 设置并创建两个独立的输出文件夹
RGB_DIR = "D:\File\Research\dataset\RGB from CDSE"
DEM_DIR = "D:\File\Research\dataset\DEM from CDSE"
os.makedirs(RGB_DIR, exist_ok=True)
os.makedirs(DEM_DIR, exist_ok=True)

# CDSE API 端点
TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
PROCESS_URL = "https://sh.dataspace.copernicus.eu/api/v1/process"

# ================= 2. 定义批量下载的区域数组 =================
# 格式: "bounds": (南纬, 北纬, 西经, 东经)
input_regions = [
    {
        "name": "Guangdong_Danxiashan", # 广东韶关 - 丹霞山世界地质公园核心区
        "bounds": (24.980, 25.080, 113.680, 113.780)
    },
    {
        "name": "Gansu_Zhangye_Qicai_Danxia", # 甘肃张掖 - 七彩丹霞景区
        "bounds": (38.900, 39.000, 100.000, 100.150)
    },
    {
        "name": "Gansu_Zhangye_Binggou_Danxia", # 甘肃张掖 - 冰沟丹霞景区
        "bounds": (38.820, 38.900, 99.840, 99.920)
    },
    {
        "name": "Jiangxi_Longhushan", # 江西鹰潭 - 龙虎山丹霞地貌核心区
        "bounds": (28.050, 28.150, 116.920, 117.020)
    },
    {
        "name": "Hunan_Langshan", # 湖南新宁 - 崀山风景名胜区（八角寨/天一巷）
        "bounds": (26.300, 26.400, 110.760, 110.860)
    },
    {
        "name": "Guizhou_Chishui", # 贵州赤水 - 佛光岩及燕子岩丹霞核心区
        "bounds": (28.350, 28.550, 105.900, 106.100)
    },
    {
        "name": "Fujian_Taining", # 福建泰宁 - 大金湖水上丹霞
        "bounds": (26.850, 26.950, 117.100, 117.200)
    },
    {
        "name": "Zhejiang_Jianglangshan", # 浙江江山 - 江郎山（三爿石）
        "bounds": (28.510, 28.560, 118.500, 118.550)
    },
    {
        "name": "Shaanxi_Jingbian_Wave_Valley", # 陕西靖边 - 波浪谷（龙洲丹霞）
        "bounds": (37.300, 37.360, 108.780, 108.860)
    },
    {
        "name": "Qinghai_Kanbula", # 青海尖扎 - 坎布拉国家森林公园丹霞区
        "bounds": (36.080, 36.180, 101.700, 101.820)
    },
    {
        "name": "Yunnan_Laojunshan_Liming", # 云南丽江 - 老君山黎明高山丹霞地貌
        "bounds": (26.920, 27.000, 99.680, 99.780)
    },
    {
        "name": "Guangxi_Bajiaozhai", # 广西资源 - 资源八角寨丹霞（湘桂交界）
        "bounds": (26.460, 26.520, 110.700, 110.780)
    },
    {
        "name": "Fujian_Guanzhoushan", # 福建连城 - 冠豸山丹霞地貌区
        "bounds": (25.700, 25.760, 116.740, 116.790)
    },
    {
        "name": "Fujian_Wuyishan", # 福建武夷山 - 天游峰/九曲溪典型丹霞区
        "bounds": (27.600, 27.700, 117.900, 118.000)
    },
    {
        "name": "Hunan_Gaoyiling", # 湖南郴州 - 高椅岭原生态丹霞
        "bounds": (25.920, 25.980, 113.080, 113.150)
    },
    {
        "name": "Hunan_Feitianshan", # 湖南郴州 - 飞天山国家地质公园
        "bounds": (25.860, 25.920, 113.060, 113.120)
    },
    {
        "name": "Chongqing_Simianshan", # 重庆江津 - 四面山丹霞地貌及瀑布群
        "bounds": (28.580, 28.680, 106.350, 106.450)
    },
    {
        "name": "Sichuan_Jianmenguan", # 四川广元 - 剑门关（砾岩型丹霞地貌）
        "bounds": (32.180, 32.260, 105.520, 105.600)
    },
    {
        "name": "Gansu_Lanzhou_Shuimo", # 甘肃兰州 - 水墨丹霞旅游景区
        "bounds": (36.080, 36.140, 103.550, 103.610)
    },
    {
        "name": "Qinghai_Guide", # 青海贵德 - 贵德国家地质公园（阿什贡七彩峰丛）
        "bounds": (36.000, 36.100, 101.350, 101.450)
    },
    {
        "name": "Xinjiang_Kuqa_Grand_Canyon", # 新疆库车 - 天山神秘大峡谷（红褐色岩溶地貌）
        "bounds": (42.100, 42.200, 83.000, 83.100)
    },
    {
        "name": "Hebei_Chengde_Qingchuifeng", # 河北承德 - 磬锤峰（北方孤立型丹霞地貌）
        "bounds": (40.970, 41.010, 117.940, 117.980)
    },
    {
        "name": "Shaanxi_Ganquan_Canyon", # 陕西甘泉 - 甘泉大峡谷（红砂岩水蚀峡谷）
        "bounds": (36.100, 36.200, 108.400, 108.500)
    },
    {
        "name": "Yunnan_Shibaoshan", # 云南剑川 - 石宝山（红砂岩龟裂石构造）
        "bounds": (26.330, 26.400, 99.800, 99.870)
    },
    {
        "name": "Gansu_Maijishan", # 甘肃天水 - 麦积山（雕刻石窟的典型丹霞石峰）
        "bounds": (34.330, 34.370, 105.980, 106.020)
    }
]

# ================= 3. 定义云端微代码 (Evalscripts) =================
# RGB 光学卫星代码 (要求返回 16位 无损数据)
EVALSCRIPT_RGB = """
//VERSION=3
function setup() {
    return {
        input: ["B04", "B03", "B02", "dataMask"],
        // 删除了 sampleType: "UINT16"，让系统默认使用 AUTO (即普通的 8位 0-255 颜色)
        output: { bands: 3 } 
    };
}
function evaluatePixel(sample) {
    // 核心魔法：直接在云端将亮度放大 2.5 倍 (这是卫星图最常用的视觉增强系数)
    return [sample.B04 * 2.5, sample.B03 * 2.5, sample.B02 * 2.5];
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
    """获取 API 访问令牌"""
    print("正在向 CDSE 请求访问令牌...")
    resp = requests.post(TOKEN_URL, data={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })
    resp.raise_for_status()
    return resp.json()["access_token"]

def calculate_unified_size(bbox):
    """
    统一计算区域的最佳像素尺寸：
    以30米为基准，确保 RGB 和 DEM 共享完全相同的尺寸，避免对齐错位。
    """
    west, south, east, north = bbox
    
    # 计算纬度跨度对应的实际物理距离 (1度纬度约等于 111000 米)
    delta_lat = north - south
    distance_meters = delta_lat * 111000
    
    # 以 10 米分辨率为基准算出真实应该有的像素
    true_pixels = distance_meters / 30.0
    
    # 寻找最接近的 2 的指数 (去掉加 1 逻辑，回归纯粹的正方形，如 512, 1024, 2048)
    power = round(math.log2(true_pixels))
    
    # 限制在合理范围内：最小 256，最大 2048
    power = max(8, min(11, power))
    target_size = 2 ** power
    
    return target_size

def download_data(name, bbox, token, data_type, target_size):
    """下载引擎：接收外部传入的统一尺寸，不再内部自行决定"""
    headers = {"Authorization": f"Bearer {token}", "Accept": "image/tiff"}
    
    # 构建 Payload，直接使用传入的 target_size
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
        return

    resp = requests.post(PROCESS_URL, headers=headers, json=payload)
    if resp.status_code == 200:
        with open(out_path, "wb") as f:
            f.write(resp.content)
        print(f"  -> 成功下载 {data_type}: {out_path}")
    else:
        print(f"  -> 下载 {data_type} 失败: 状态码 {resp.status_code}")
        print(resp.text)

# ================= 5. 执行主循环 =================
if __name__ == "__main__":
    token = fetch_token()
    print(f"\n成功获取 Token！准备批量处理 {len(input_regions)} 个地貌区域...\n")
    
    for idx, region in enumerate(input_regions, 1):
        name = region["name"]
        south, north, west, east = region["bounds"]
        
        # 组装 CDSE 要求的 bbox 顺序
        bbox_cdse = [west, south, east, north]
        
        # 💡 核心改动：在主循环里计算一次统一的尺寸
        unified_size = calculate_unified_size(bbox_cdse)
        
        print(f"\n[{idx}/{len(input_regions)}] 正在处理: {name}")
        print(f"  -> 已计算统一网格分辨率: {unified_size} x {unified_size}")
        
        # 将统一的尺寸同时传给 DEM 和 RGB 下载函数
        download_data(name, bbox_cdse, token, "DEM", unified_size)
        download_data(name, bbox_cdse, token, "RGB", unified_size)
        
        time.sleep(1)
        
    print("\n🎉 全部数据批处理下载完成！")