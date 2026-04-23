import geopandas as gpd
from shapely.geometry import box
import os

# ================= 1. 输入数据区 =================
# 统一格式: "bounds": (south, north, west, east) 即 (南纬, 北纬, 西经, 东经)
input_regions = [
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
    },

    # ========== 北美洲 (North America) ==========
    {
        "name": "Grand_Canyon_USA", # 科罗拉多大峡谷 (美国亚利桑那州)
        "bounds": (35.800, 36.400, -113.800, -111.800)
    },
    {
        "name": "Copper_Canyon_Mexico", # 铜峡谷 (墨西哥) - 比美国大峡谷更深更长
        "bounds": (27.100, 27.800, -108.200, -107.500)
    },
    {
        "name": "Zion_Canyon_USA", # 锡安峡谷 (美国犹他州)
        "bounds": (37.200, 37.350, -113.050, -112.900)
    },
    {
        "name": "Palo_Duro_Canyon", # 帕洛杜罗峡谷 (美国得克萨斯州) - 美国第二大峡谷
        "bounds": (34.850, 35.050, -101.750, -101.550)
    },

    # ========== 南美洲 (South America) ==========
    {
        "name": "Colca_Canyon_Peru", # 科尔卡大峡谷 (秘鲁) - 世界最深峡谷之一
        "bounds": (-15.750, -15.500, -72.050, -71.550)
    },
    {
        "name": "Cotahuasi_Canyon_Peru", # 科塔瓦西峡谷 (秘鲁)
        "bounds": (-15.350, -15.100, -73.100, -72.800)
    },

    # ========== 欧洲 (Europe) ==========
    {
        "name": "Tara_River_Canyon", # 塔拉河峡谷 (黑山共和国) - 欧洲最深峡谷
        "bounds": (43.100, 43.350, 18.900, 19.300)
    },
    {
        "name": "Verdon_Gorge_France", # 凡尔登大峡谷 (法国)
        "bounds": (43.700, 43.850, 6.300, 6.500)
    },
    {
        "name": "Thingvellir_Rift_Iceland", # 辛格韦德利大裂谷 (冰岛) - 大西洋中脊露出海面的裂谷带
        "bounds": (64.200, 64.350, -21.250, -21.000)
    }
    # 可以在这里无限添加你的地貌数据...
]

print(f"开始为 {len(input_regions)} 个地貌区域构建地理几何体...")

# ================= 2. 数据转换区 =================
names = []
geometries = []

for region in input_regions:
    names.append(region["name"])
    
    # 解析你的 bounds 数据 (南, 北, 西, 东)
    south, north, west, east = region["bounds"]
    
    # ⚠️ 关键点：shapely 的 box 函数需要的参数顺序严格是 (minx, miny, maxx, maxy)
    # 也就是 (西经, 南纬, 东经, 北纬)
    rect = box(west, south, east, north)
    
    geometries.append(rect)

# ================= 3. 生成与导出区 =================
# 组装成地理数据框
gdf = gpd.GeoDataFrame({
    "name": names,
    "geometry": geometries
})

# 定义坐标系为 WGS84 (经纬度)
gdf.set_crs(epsg=4326, inplace=True)

# 导出为 Shapefile
output_folder = "D:/File/Research/dataset/NASA"
os.makedirs(output_folder, exist_ok=True)
output_path = os.path.join(output_folder, "target_landforms.shp")

print(f"正在导出为 Shapefile: {output_path} ...")
gdf.to_file(output_path)

print("生成成功！快把生成的四个同名文件打包成 .zip 提交给 NASA 吧！")