import os
from pathlib import Path
from tqdm import tqdm

INPUT = r"E:\WorkSpace\Data\unet\txt"

def extract_category(text: str) -> str:
    # ... (你原本的 extract_category 逻辑完全保留，不用动) ...
    t = text.lower()
    if any(w in t for w in ['glacier','icefield','ice','snow','alpine','crevasse','iceberg','frozen','icefall']):
        return 'ice_mountain'
    if any(w in t for w in ['yardang','wind eroded','aeolian','wind-carved','wind eroded ridge']):
        return 'yardang'
    if any(w in t for w in ['karst','limestone','sinkhole','cave','doline','stalactite','tower karst']):
        return 'karst'
    if any(w in t for w in ['loess','plateau','gully','terrace','yellow earth','silt','ravine']):
        return 'loess'
    if any(w in t for w in ['danxia','red bed','sandstone cliff','mesa','butte','red rock']):
        return 'danxia'
    if any(w in t for w in ['dune','sand','barchan','crescent','linear dune','erg','dune field','sand sea',
                            'desert','arid','salt','taklamakan','kumtag','sahara','wadi','namib','atacama',
                            'death valley','dasht','simpson','empty quarter','hyperarid','rocky desert','sandstone','badain']):
        return 'desert'
    if any(w in t for w in ['mountain','peak','ridge','cliff','rocky','yosemite','matterhorn','cook','fitz',
                            'everest','tomur','columbia','rockies','alps','summit']):
        return 'ice_mountain' if any(w in t for w in ['snow','ice','glacier']) else 'mountain'
    return 'general'


def main():
    # 1. 避免使用内置函数 input 作为变量名，改用 input_dir
    input_dir = Path(INPUT)

    # 2. 增加安全过滤，只获取 .txt 文件，防止把文件夹或其他文件读进来
    files = [f for f in input_dir.iterdir() if f.is_file() and f.suffix == '.txt']

    for file in tqdm(files, desc='Processing Prompts'):
        
        # 3. 读取原始内容
        original_text = file.read_text(encoding="utf-8")
        
        # 4. 关键：如果是根据文件内容分类，应该传 original_text；如果是根据文件名，传 file.name
        # 这里我假设你其实是想根据里面的原有 prompt 内容来分类
        category = extract_category(original_text) 
        
        # 5. 生成前缀 (极简写法)
        if category == 'general':
            prefix = "This is a general terrain; "
        else:
            prefix = f"This is a terrain named {category}; "

        # 6. 安全拦截：如果已经被处理过了，就跳过 (防止重复运行套娃)
        if original_text.startswith("This is a terrain"):
            continue

        # 7. 执行写入
        file.write_text(prefix + original_text, encoding='utf-8')

if __name__ == "__main__":  
    main()