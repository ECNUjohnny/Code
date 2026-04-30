import os

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
# 将 7890 替换成你樱花猫里查到的真实端口号
# os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"
# os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"

import io
import geopandas as gpd
from datasets import load_dataset, Image as HFImage
from PIL import Image as PILImage
from huggingface_hub import login
from dotenv import load_dotenv

# 1. 登录与初始化
load_dotenv()
login(token=os.getenv("HUGGINGFACE_CLIENT_TOKEN"))
 
# 2. 目标区域 (boxes)
areas = [
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

    # ========== 全球超级大都市 ==========
    {
        "name": "Tokyo_Metropolitan", # 东京都 - 核心都会区 (亚洲)
        "bounds": (35.580, 35.780, 139.590, 139.790)
    },
    {
        "name": "New_York_Manhattan", # 纽约曼哈顿岛及周边 (北美洲)
        "bounds": (40.650, 40.850, -74.100, -73.900)
    },
    {
        "name": "Paris_City_Center", # 巴黎 - 城市中心区 (欧洲)
        "bounds": (48.760, 48.960, 2.240, 2.440)
    },
    {
        "name": "London_Greater_Area", # 大伦敦地区 (欧洲)
        "bounds": (51.400, 51.600, -0.220, -0.020)
    },
    {
        "name": "Beijing_Core_Area", # 北京 - 城市中心环线区 (亚洲)
        "bounds": (39.810, 40.010, 116.290, 116.490)
    },
    {
        "name": "Sao_Paulo_Center", # 圣保罗 - 城市密集区 (南美洲)
        "bounds": (-23.650, -23.450, -46.730, -46.530)
    },
    {
        "name": "Cairo_Urban_Giza", # 开罗与吉萨交界带 (非洲)
        "bounds": (29.880, 30.080, 31.030, 31.230)
    },
    {
        "name": "Sydney_Harbour", # 悉尼港湾区 (大洋洲)
        "bounds": (-33.960, -33.760, 151.100, 151.300)
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

# 3. 本地索引筛选
print("加载空间索引...")
gdf = gpd.read_parquet("D:/File/Research/dataset/land_s2.parquet")
id_map = {}  # 记录 ID 对应哪个区域

for a in areas:
    name, (lat_min, lat_max, lon_min, lon_max) = a["name"], a["bounds"]
    sub_gdf = gdf.cx[lon_min:lon_max, lat_min:lat_max]
    ids = sub_gdf['id'].tolist()
    
    for i in ids: id_map[i] = name
        
    os.makedirs("D:/File/Research/dataset/DEM_from_TOM", exist_ok=True)
    os.makedirs("D:/File/Research/dataset/RGB_from_TOM", exist_ok=True)
    print(f"🌍 [{name}] 找到 {len(ids)} 个网格。")

total = len(id_map)
if total == 0: exit(print("未找到目标！"))

# ==========================================
# 4. 极速下载：DEM 高程图
# ==========================================
print(f"\n🚀 开始极速下载 {total} 张 DEM...")
dem_ds = load_dataset("Major-TOM/Core-DEM", split="train", streaming=True)
dem_ds = dem_ds.select_columns(['grid_cell', 'DEM'])
dem_ds = dem_ds.cast_column("DEM", HFImage(decode=False)) # 关闭解码提速

found = 0
scan_cnt = 0

for item in dem_ds:
    scan_cnt += 1
    if scan_cnt % 5000 == 0: print(f"⏳ 扫描中... 已过滤 {scan_cnt} 个", end='\r')

    cid = item.get('grid_cell')
    if cid in id_map:
        path = f"D:/File/Research/dataset/DEM_from_TOM/{cid}.tif"
        with open(path, "wb") as f:
            f.write(item['DEM']['bytes']) # 直接写入二进制
            
        found += 1
        print(f"\n✅ [DEM] ({found}/{total}) {cid} -> {id_map[cid]}")
        if found >= total: break

# ==========================================
# 5. 极速下载：S2 卫星图
# ==========================================
print("\n🚀 开始极速下载 S2 卫星图...")
s2_ds = load_dataset("Major-TOM/Core-S2L2A", split="train", streaming=True)
s2_ds = s2_ds.select_columns(['grid_cell', 'B04', 'B03', 'B02'])
for b in ['B04', 'B03', 'B02']: s2_ds = s2_ds.cast_column(b, HFImage(decode=False))

found = 0
scan_cnt = 0

for item in s2_ds:
    scan_cnt += 1
    if scan_cnt % 5000 == 0: print(f"⏳ 扫描中... 已过滤 {scan_cnt} 个", end='\r')

    cid = item.get('grid_cell')
    if cid in id_map:
        path = f"D:/File/Research/dataset/RGB_from_TOM/{cid}.jpg"
        
        # 懒解码：只有命中目标才在内存中转换图片
        r = PILImage.open(io.BytesIO(item['B04']['bytes']))
        g = PILImage.open(io.BytesIO(item['B03']['bytes']))
        b = PILImage.open(io.BytesIO(item['B02']['bytes']))

        PILImage.merge("RGB", (r, g, b)).save(path)
        
        found += 1
        print(f"\n✅ [S2] ({found}/{total}) {cid} -> {id_map[cid]}")
        if found >= total: break

print("\n🏆 全部搞定！")