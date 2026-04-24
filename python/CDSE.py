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
        "name": "Yarlung_Tsangpo_Core_Horseshoe", # 雅鲁藏布大峡谷 - 果果塘大拐弯/马蹄形核心区
        "bounds": (29.600, 29.700, 94.900, 95.000)
    },
    {
        "name": "Tiger_Leaping_Gorge_Core", # 云南虎跳峡 - 最狭窄的上虎跳至中虎跳地段
        "bounds": (27.200, 27.300, 100.120, 100.220)
    },
    {
        "name": "Enshi_Grand_Canyon_Core", # 湖北恩施大峡谷 - 一炷香及绝壁长廊核心段
        "bounds": (30.400, 30.500, 109.150, 109.250)
    },
    {
        "name": "Tianshan_Mysterious_Canyon", # 新疆天山神秘大峡谷（库车大峡谷）最深处
        "bounds": (42.150, 42.250, 83.000, 83.100)
    },

    # ========== 北美洲顶级峡谷群核心区 ==========
    {
        "name": "Grand_Canyon_Bright_Angel", # 科罗拉多大峡谷 - 光明天使步道及最深峡谷区
        "bounds": (36.050, 36.150, -112.200, -112.100)
    },
    {
        "name": "Glen_Canyon_Horseshoe_Bend", # 格伦峡谷 - 著名的马蹄湾极度弯曲处
        "bounds": (36.820, 36.920, -111.560, -111.460)
    },
    {
        "name": "Zion_Canyon_Angels_Landing", # 锡安峡谷 - 天使降临处及最陡峭的岩壁区
        "bounds": (37.230, 37.330, -112.980, -112.880)
    },
    {
        "name": "Waimea_Canyon_Hawaii", # 夏威夷威美亚峡谷 - 太平洋大峡谷核心切割区
        "bounds": (22.030, 22.130, -159.680, -159.580)
    },
    {
        "name": "Copper_Canyon_Urique", # 墨西哥铜峡谷 - 乌里克峡谷最深落差段
        "bounds": (27.170, 27.270, -107.930, -107.830)
    },

    # ========== 欧洲顶级峡谷核心区 ==========
    {
        "name": "Verdon_Gorge_Point_Sublime", # 法国凡尔登大峡谷 - 崇高点（最深切的石灰岩裂缝）
        "bounds": (43.720, 43.820, 6.340, 6.440)
    },
    {
        "name": "Tara_River_Canyon_Core", # 黑山塔拉河峡谷 - 大桥及最深河谷区
        "bounds": (43.120, 43.220, 19.250, 19.350)
    },

    # ========== 非洲大峡谷核心区 ==========
    {
        "name": "Fish_River_Hells_Bend", # 纳米比亚鱼河大峡谷 - 地狱之弯（极度曲折深切的河谷）
        "bounds": (-27.630, -27.530, 17.550, 17.650)
    },
    {
        "name": "Blyde_River_Three_Rondavels", # 南非布莱德河峡谷 - 三茅庐奇观及大拐弯
        "bounds": (-24.600, -24.500, 30.750, 30.850)
    },
    {
        "name": "Todra_Gorge_Morocco", # 摩洛哥托德拉峡谷 - 极度狭窄的干旱区裂谷
        "bounds": (31.540, 31.640, -5.630, -5.530)
    },
    {
        "name": "Hells_Gate_Kenya", # 肯尼亚地狱之门国家公园 - 东非大裂谷内的狭窄峡谷支脉
        "bounds": (-0.950, -0.850, 36.300, 36.400)
    },

    # ========== 南美洲大峡谷核心区 ==========
    {
        "name": "Colca_Canyon_Condor_Cross", # 秘鲁科尔卡大峡谷 - 秃鹰十字架（高差达3000米的极深切口）
        "bounds": (-15.650, -15.550, -71.930, -71.830)
    }
    # 在这里可以继续添加几十上百个区域...
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

def download_data(name, bbox, token, data_type):
    """强制正方形引擎：专为 Unity 地形底层架构适配"""
    headers = {"Authorization": f"Bearer {token}", "Accept": "image/tiff"}
    
    # 💡 核心魔法：Unity 适配器
    # 卫星贴图(RGB)用 1024，高程图(DEM)为了迎合 2^n+1 的网格顶点规律，直接强制设为 1025
    target_size = 1024 if data_type == "DEM" else 1024
    
    print(f"  -> 正在以 {target_size}x{target_size} 的 Unity 标准分辨率下载 {data_type}...")

    # 构建强制正方形 Payload
    payload = {
        "input": {
            "bounds": {
                "bbox": bbox,
                "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"}
            },
            "data": []
        },
        "output": {
            # 放弃自动比例，强行锁死正方形分辨率
            "width": target_size,
            "height": target_size,
            "responses": [{"identifier": "default", "format": {"type": "image/tiff"}}]
        }
    }

    # 根据请求类型动态配置数据源和微代码
    if data_type == "RGB":
        payload["input"]["data"] = [{
            "type": "sentinel-2-l2a",
            "dataFilter": {
                "timeRange": {"from": "2021-01-01T00:00:00Z", "to": "2025-12-31T23:59:59Z"},
                "maxCloudCoverage": 5 # 给足一年的时间，寻找 5% 以下云量的完美晴空图
            }
        }]
        payload["evalscript"] = EVALSCRIPT_RGB
        out_path = os.path.join(RGB_DIR, f"{name}_RGB.tif")
        
    elif data_type == "DEM":
        payload["input"]["data"] = [{"type": "dem"}]
        payload["evalscript"] = EVALSCRIPT_DEM
        out_path = os.path.join(DEM_DIR, f"{name}_DEM.tif")

    # 如果文件已经存在，支持断点续传（跳过下载）
    if os.path.exists(out_path):
        print(f"  -> {data_type} 已存在，跳过。")
        return

    # 发送请求
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
        
        # ⚠️ 关键点：CDSE API 的 bbox 参数顺序必须是 [西经, 南纬, 东经, 北纬]
        bbox_cdse = [west, south, east, north]
        
        print(f"[{idx}/{len(input_regions)}] 正在处理: {name}")
        
        # 依次请求并下载该区域的两种模态数据
        download_data(name, bbox_cdse, token, "DEM")
        download_data(name, bbox_cdse, token, "RGB")
        
        # 礼貌性延迟：避免并发请求过快被服务器封禁 IP (Rate Limiting)
        time.sleep(2)
        
    print("\n🎉 全部数据批处理下载完成！请检查 RGB 和 DEM 文件夹。")