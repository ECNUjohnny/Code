import os
import requests
import time
import math
from dotenv import load_dotenv

# ================= 1. 环境与路径配置 =================
load_dotenv()
CLIENT_ID = os.getenv("CDSE_CLIENT_ID")
CLIENT_SECRET = os.getenv("CDSE_CLIENT_SECRET")

#print(os.getenv("CDSE_CLIENT_ID"))

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
    # ========== 世界著名高山与峰顶 ==========
    {
        "name": "Mount_Everest_Peak", # 珠穆朗玛峰 - 核心主峰区 (亚洲)
        "bounds": (27.850, 28.050, 86.750, 86.950)
    },
    {
        "name": "Mount_Kilimanjaro", # 乞力马扎罗山 - 火山口 (非洲)
        "bounds": (-3.160, -2.960, 37.250, 37.450)
    },
    {
        "name": "Mount_Fuji", # 富士山 - 顶部区域 (亚洲)
        "bounds": (35.260, 35.460, 138.630, 138.830)
    },
    {
        "name": "Mont_Blanc", # 勃朗峰 - 阿尔卑斯山脉 (欧洲)
        "bounds": (45.730, 45.930, 6.760, 6.960)
    },
    {
        "name": "Mount_Denali", # 迪纳利山 - 北美最高峰 (北美洲)
        "bounds": (62.970, 63.170, -151.100, -150.900)
    },
    {
        "name": "Aconcagua", # 阿空加瓜山 - 安第斯山脉 (南美洲)
        "bounds": (-32.750, -32.550, -70.110, -69.910)
    },
    {
        "name": "Mount_Elbrus", # 厄尔布鲁士山 - 高加索山脉 (欧洲)
        "bounds": (43.250, 43.450, 42.340, 42.540)
    },

    # ========== 极端干旱与沙漠区 ==========
    {
        "name": "Sahara_Desert_Dunes", # 撒哈拉沙漠 - 沙丘群 (非洲)
        "bounds": (23.000, 23.200, 11.000, 11.200)
    },
    {
        "name": "Atacama_Desert", # 阿塔卡马沙漠 - 极旱区 (南美洲)
        "bounds": (-24.100, -23.900, -69.600, -69.400)
    },
    {
        "name": "Namib_Desert_Namibia", # 纳米布沙漠 - 红色沙丘 (非洲)
        "bounds": (-24.800, -24.600, 15.300, 15.500)
    },
    {
        "name": "Taklamakan_Desert", # 塔克拉玛干沙漠 - 流动沙丘 (亚洲)
        "bounds": (39.000, 39.200, 80.000, 80.200)
    },
    {
        "name": "Death_Valley", # 死谷 - 北美最低点 (北美洲)
        "bounds": (36.150, 36.350, -116.900, -116.700)
    },
    {
        "name": "Rub_al_Khali", # 鲁卜哈利沙漠 - 阿拉伯半岛 (亚洲)
        "bounds": (20.000, 20.200, 50.000, 50.200)
    },
    {
        "name": "Simpson_Desert", # 辛普森沙漠 - 红色中心 (大洋洲)
        "bounds": (-24.600, -24.400, 137.400, 137.600)
    },

    # ========== 茂密森林与热带雨林 ==========
    {
        "name": "Amazon_Rainforest_Core", # 亚马逊雨林 - 核心区 (南美洲)
        "bounds": (-3.100, -2.900, -60.100, -59.900)
    },
    {
        "name": "Congo_Basin", # 刚果盆地热带雨林 (非洲)
        "bounds": (1.000, 1.200, 23.000, 23.200)
    },
    {
        "name": "Daintree_Rainforest", # 戴恩树雨林 (大洋洲)
        "bounds": (-16.300, -16.100, 145.300, 145.500)
    },
    {
        "name": "Taiga_Siberia", # 西伯利亚泰加林 - 针叶林 (亚洲)
        "bounds": (62.000, 62.200, 110.000, 110.200)
    },
    {
        "name": "Black_Forest", # 黑森林 - 温带森林 (欧洲)
        "bounds": (48.250, 48.450, 8.050, 8.250)
    },
    {
        "name": "Sequoia_National_Park", # 红杉树国家公园 (北美洲)
        "bounds": (36.450, 36.650, -118.850, -118.650)
    },
    {
        "name": "Borneo_Rainforest", # 婆罗洲热带雨林 (亚洲)
        "bounds": (2.400, 2.600, 114.000, 114.200)
    },

    # ========== 独特高程地貌与火山 (替换了之前的城市) ==========
    {
        "name": "Meteor_Crater", # 巴林杰陨石坑 - 极度规整的巨大凹陷 (北美洲)
        "bounds": (34.930, 35.130, -111.120, -110.920)
    },
    {
        "name": "Mount_St_Helens", # 圣海伦斯火山 - 马蹄形火山口 (北美洲)
        "bounds": (46.100, 46.300, -122.290, -122.090)
    },
    {
        "name": "Mount_Vesuvius", # 维苏威火山 - 复杂的双层火山口 (欧洲)
        "bounds": (40.720, 40.920, 14.330, 14.530)
    },
    {
        "name": "Mount_Roraima", # 罗赖马山 - 边缘极其陡峭的平顶桌状山 (南美洲)
        "bounds": (5.090, 5.290, -60.830, -60.630)
    },
    {
        "name": "Sognefjord_Norway", # 松恩峡湾 - 极深的海蚀峡湾与高耸悬崖 (欧洲)
        "bounds": (60.830, 61.030, 6.900, 7.100)
    },
    {
        "name": "Milford_Sound", # 米尔福德峡湾 - 高落差冰川地貌 (大洋洲)
        "bounds": (-44.740, -44.540, 167.790, 167.990)
    },
    {
        "name": "Guilin_Karst", # 桂林阳朔 - 密集的喀斯特峰林 (亚洲)
        "bounds": (24.680, 24.880, 110.400, 110.600)
    },
    {
        "name": "Blyde_River_Canyon", # 布莱德河峡谷 - 巨大的绿色峡谷切割 (非洲)
        "bounds": (-24.680, -24.480, 30.710, 30.910)
    },

    # ========== 峡谷、地貌与奇观 ==========
    {
        "name": "Grand_Canyon", # 科罗拉多大峡谷 (北美洲)
        "bounds": (36.000, 36.200, -112.250, -112.050)
    },
    {
        "name": "Yarlung_Tsangpo_Canyon", # 雅鲁藏布大峡谷 (亚洲)
        "bounds": (29.450, 29.650, 94.900, 95.100)
    },
    {
        "name": "Uluru_Ayers_Rock", # 乌鲁鲁巨岩 (大洋洲)
        "bounds": (-25.450, -25.250, 130.950, 131.150)
    },
    {
        "name": "Salar_de_Uyuni", # 乌尤尼盐沼 (南美洲)
        "bounds": (-20.300, -20.100, -67.700, -67.500)
    },
    {
        "name": "Yellowstone_Caldera", # 黄石国家公园火山口地貌 (北美洲)
        "bounds": (44.350, 44.550, -110.650, -110.450)
    },
    {
        "name": "Danxia_Landform_Zhangye", # 张掖丹霞地貌 (亚洲)
        "bounds": (38.850, 39.050, 99.950, 100.150)
    },
    {
        "name": "Richat_Structure", # 撒哈拉之眼 (非洲)
        "bounds": (21.020, 21.220, -11.500, -11.300)
    },

    # ========== 河口三角洲与广阔湿地 ==========
    {
        "name": "Nile_Delta", # 尼罗河三角洲农田水网 (非洲)
        "bounds": (31.350, 31.550, 30.950, 31.150)
    },
    {
        "name": "Mississippi_Delta", # 密西西比河三角洲 (北美洲)
        "bounds": (29.150, 29.350, -89.350, -89.150)
    },
    {
        "name": "Ganges_Brahmaputra_Delta", # 恒河-布拉马普特拉河三角洲 (亚洲)
        "bounds": (21.850, 22.050, 89.450, 89.650)
    },
    {
        "name": "Mekong_Delta", # 湄公河三角洲 (亚洲)
        "bounds": (9.850, 10.050, 105.850, 106.050)
    },
    {
        "name": "Okavango_Delta", # 奥卡万戈内陆三角洲 (非洲)
        "bounds": (-19.550, -19.350, 22.750, 22.950)
    },
    {
        "name": "Everglades_Wetland", # 大沼泽地国家公园 (北美洲)
        "bounds": (25.650, 25.850, -80.750, -80.550)
    },
    {
        "name": "Yellow_River_Delta", # 黄河三角洲入海口 (亚洲)
        "bounds": (37.650, 37.850, 119.050, 119.250)
    },

    # ========== 冰川与极地风貌 ==========
    {
        "name": "Jakobshavn_Glacier", # 雅各布港冰川 (北美洲/格陵兰)
        "bounds": (69.050, 69.250, -49.650, -49.450)
    },
    {
        "name": "Vatnajokull_Glacier", # 瓦特纳冰川 (欧洲/冰岛)
        "bounds": (64.250, 64.450, -16.850, -16.650)
    },
    {
        "name": "Perito_Moreno_Glacier", # 莫雷诺冰川 (南美洲)
        "bounds": (-50.550, -50.350, -73.150, -72.950)
    },
    {
        "name": "Lambert_Glacier", # 兰伯特冰川 - 世界最大冰川之一 (南极洲)
        "bounds": (-71.600, -71.400, 67.900, 68.100)
    },
    {
        "name": "Svalbard_Archipelago", # 斯瓦尔巴群岛极地带 (欧洲)
        "bounds": (78.150, 78.350, 15.450, 15.650)
    },
    {
        "name": "Aletsch_Glacier", # 阿莱奇冰川 (欧洲)
        "bounds": (46.350, 46.550, 7.950, 8.150)
    },
    {
        "name": "McMurdo_Dry_Valleys", # 麦克默多干燥谷 (南极洲)
        "bounds": (-77.600, -77.400, 161.900, 162.100)
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