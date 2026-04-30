from datasets import load_dataset

# 流式拉取 DEM 仓库的第一条数据
dem_dataset = load_dataset("Major-TOM/Core-S2L2A", split="train", streaming=True)
first_item = next(iter(dem_dataset))

# 打印出它所有的字段名
print("Core-DEM 包含的字段有：")
print(first_item.keys())