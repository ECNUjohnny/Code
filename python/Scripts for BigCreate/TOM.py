import os
import geopandas as gpd
from datasets import load_dataset
from huggingface_hub import login
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

TOKEN = os.getenv("HUGGINGFACE_CLIENT_TOKEN")

login(token = TOKEN)

# ==========================================
# 1. 配置区域参数
# 结构：(min_lat, max_lat, min_lon, max_lon)
# ==========================================
input_regions = [
    {
        "name": "Mount_Everest_Peak", 
        "bounds": (27.850, 28.050, 86.750, 86.950)
    },
    {
        "name": "Mount_Kilimanjaro", 
        "bounds": (-3.160, -2.960, 37.250, 37.450)
    },
]

# ==========================================
# 2. 本地计算：生成全局分拣“通讯录”
# ==========================================
print("正在加载全球空间索引...")
gdf = gpd.read_parquet("D:\File\Research\dataset\land_s2.parquet")

# 这个字典用于记录：网格 ID -> 归属哪个区域 (例如：'MT10_0U_38R' -> 'Mount_Everest_Peak')
target_id_to_region = {}

print("\n开始空间计算与筛选...")
for region in input_regions:
    name = region["name"]
    # 按照你给的数组解包出经纬度
    min_lat, max_lat, min_lon, max_lon = region["bounds"]
    
    # 注意 GeoPandas 的 cx 语法是 [lon:lon, lat:lat] 也就是 [经度, 纬度]
    region_gdf = gdf.cx[min_lon:max_lon, min_lat:max_lat]
    region_ids = region_gdf['id'].tolist()
    
    # 存入全局字典
    for grid_id in region_ids:
        target_id_to_region[grid_id] = name
        
    # 为每座山峰创建专属的文件夹结构
    os.makedirs(f"D:\File\Research\dataset\DEM from TOM", exist_ok=True)
    os.makedirs(f"D:\File\Research\dataset\RGB from TOM", exist_ok=True)
    
    print(f"🌍 区域 [{name}] 框选出 {len(region_ids)} 个目标网格。")

total_targets = len(target_id_to_region)
print(f"\n✅ 汇总完毕！总共需要从云端下载 {total_targets} 张图片。")

if total_targets == 0:
    print("没有找到任何目标，请检查您的经纬度是否正确（留意正负号）。")
    exit()

# ==========================================
# 3. 单次全量遍历：流水线分拣下载 (DEM部分)
# ==========================================
print("\n🚀 开始流水线获取 DEM 高度图...")
dem_dataset = load_dataset("Major-TOM/Core-DEM", split="train", streaming=True)
dem_found = 0

for item in dem_dataset:
    current_id = item['grid_cell']
    
    # 如果当前 ID 在我们的全局通讯录里
    if current_id in target_id_to_region:
        region_name = target_id_to_region[current_id]
        save_path = f"D:\File\Research\dataset\DEM from TOM\{current_id}.tif"
        
        # 保存图片
        item['DEM'].save(save_path)
        dem_found += 1
        print(f"  [DEM 获取成功] ({dem_found}/{total_targets}) {current_id} -> 📁 {region_name}")
        
        # 找齐了就立刻停止网络流，不再多浪费一秒钟
        if dem_found >= total_targets:
            print("🎉 所有区域的 DEM 高度图提取完毕！")
            break

# ==========================================
# 4. 单次全量遍历：流水线分拣下载 (S2 卫星图部分)
# ==========================================
print("\n🚀 开始流水线获取 Sentinel-2 彩色卫星图...")
s2_dataset = load_dataset("Major-TOM/Core-S2L2A", split="train", streaming=True)
s2_found = 0

for item in s2_dataset:
    current_id = item['grid_cell']
    
    if current_id in target_id_to_region:
        region_name = target_id_to_region[current_id]
        # 卫星图通常保存为 jpg 或 png，视 Hugging Face 的原始格式而定
        save_path = f"D:\File\Research\dataset\RGB from TOM\{current_id}.jpg"
        
        # 💡注意：这里假设图像字段名叫 'image' (HF 默认视觉字段)。
        # 如果报错 KeyError，请改成 item['S2'] 或你刚才用 print 看出来的对应字段名。
        item['image'].save(save_path)
        
        s2_found += 1
        print(f"  [S2 获取成功] ({s2_found}/{total_targets}) {current_id} -> 📁 {region_name}")
        
        if s2_found >= total_targets:
            print("🎉 所有区域的 S2 彩色卫星图提取完毕！")
            break

print("\n🏆 所有下载任务圆满结束！你的数据集已经按山峰名字分类整理好了！")