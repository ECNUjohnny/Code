import os
import requests
import time
from dotenv import load_dotenv

# ================= 1. 环境与路径配置 =================
load_dotenv()
CLIENT_ID = os.getenv("CDSE_CLIENT_ID")
CLIENT_SECRET = os.getenv("CDSE_CLIENT_SECRET")

# 设置并创建两个独立的输出文件夹
RGB_DIR = "./Dataset_CDSE_RGB"
DEM_DIR = "./Dataset_CDSE_DEM"
os.makedirs(RGB_DIR, exist_ok=True)
os.makedirs(DEM_DIR, exist_ok=True)

# CDSE API 端点
TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
PROCESS_URL = "https://sh.dataspace.copernicus.eu/api/v1/process"

# ================= 2. 定义批量下载的区域数组 =================
# 格式: "bounds": (南纬, 北纬, 西经, 东经)
input_regions = [
    {
        "name": "Thingvellir_Rift", # 冰岛大裂谷
        "bounds": (64.200, 64.350, -21.250, -21.000)
    },
    {
        "name": "Danxia_Mountain",  # 丹霞山
        "bounds": (24.863, 25.070, 113.607, 113.798)
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
        output: { bands: 3, sampleType: "UINT16" }
    };
}
function evaluatePixel(sample) {
    return [sample.B04, sample.B03, sample.B02];
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
    """通用下载引擎，根据 data_type 决定下 RGB 还是 DEM"""
    headers = {"Authorization": f"Bearer {token}", "Accept": "image/tiff"}
    
    # 基础 Payload 框架
    payload = {
        "input": {
            "bounds": {
                "bbox": bbox,
                "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"}
            },
            "data": [] # 数据源将根据请求类型动态填充
        },
        "output": {
            "width": 1024,  # 统一将图片重采样为 512x512
            "height": 1024,
            "responses": [{"identifier": "default", "format": {"type": "image/tiff"}}]
        }
    }

    # 根据请求类型动态配置数据源和微代码
    if data_type == "RGB":
        payload["input"]["data"] = [{
            "type": "sentinel-2-l2a",
            "dataFilter": {
                "timeRange": {"from": "2023-07-01T00:00:00Z", "to": "2023-08-31T23:59:59Z"},
                "maxCloudCoverage": 10 # 剔除云层
            }
        }]
        payload["evalscript"] = EVALSCRIPT_RGB
        out_path = os.path.join(RGB_DIR, f"{name}_RGB.tif")
        
    elif data_type == "DEM":
        payload["input"]["data"] = [{"type": "copernicus-dem"}]
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