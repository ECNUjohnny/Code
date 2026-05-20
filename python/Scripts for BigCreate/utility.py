import os
from tqdm import tqdm
import shutil
from pathlib import Path

# ==========================================
# 1. 配置区
# ==========================================
INPUT = r"D:\WorkSpace\Data\Yadan\Yadan"
OUTPUT = r"D:\WorkSpace\Data\Yadan"

# 存放你需要匹配的字符串（关键词）。
# 虽然你原来写的是 {}，但我建议这里用列表 [] 或集合 {} 存放关键词更直观。
# 如果你坚持用字典，这段代码依然有效（它会自动匹配字典的键 key）。
mp = ["Lenghu_Yardang_Qaidam_Qinghai", 
      "Wusute_Water_Yardang_Qaidam_Qinghai", 
      "Dunhuang_Yardang_Geopark_Gansu", 
      "Bailongdui_Yardang_LopNur_Xinjiang",
      "Urho_Ghost_City_Karamay_Xinjiang",
      "Kaluts_Mega_Yardang_Lut_Desert_Iran",
      "Borkou_Mega_Yardang_Sahara_Chad",
      "White_Desert_Yardang_Farafra_Egypt",
      "Kharga_Linear_Yardang_Egypt",
      "Ica_Valley_Coastal_Yardang_Peru",
      "Pumice_Stone_Yardang_Argentina",
    ] 


def process():
    input_path = Path(INPUT)
    output_path = Path(OUTPUT)

    # 确保总的输出目录是存在的
    output_path.mkdir(parents=True, exist_ok=True)

    subdirs = [d for d in input_path.iterdir() if d.is_dir()]

    print(f"发现 {len(subdirs)} 个数据子文件夹，开始提取与重组...\n")

    cnt = 0

    # ==========================================
    # 2. 核心遍历与匹配逻辑
    # ==========================================
    for subdir in tqdm(subdirs, desc="处理进度"):
        folder_name = subdir.name

        # 核心魔法：判断 folder_name 中是否包含 mp 里的任意一个关键词
        if any(keyword in folder_name for keyword in mp):
            
            # 拼装目标路径
            target_path = output_path / folder_name

            # 复制整个文件夹到指定位置
            cnt += 1
            
            if not target_path.exists():
                # shutil.copytree 专门用于复制整个文件夹（包括里面的所有文件）
                shutil.copytree(subdir, target_path)
            else:
                # 为了不打断 tqdm 进度条，这里用 tqdm.write 打印提示（可选）
                # tqdm.write(f"跳过：{folder_name} (目标文件夹已存在)")
                pass

    print(f"{cnt}文件夹已经复制")

if __name__ == "__main__": # 注意这里需要加下划线
    process()