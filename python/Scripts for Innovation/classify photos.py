import os
import shutil
import json
from tqdm import tqdm

cat2folder = dict()

CATEGORY = r'D:\WorkSpace\Research\Innovation institute\Data\Video Gen\categories'
SOURCE = r'D:\WorkSpace\Research\Innovation institute\Data\Video Gen\scenes'
TARGET = r'D:\WorkSpace\Research\Innovation institute\Data\Video Gen'

def init():
    with os.scandir(CATEGORY) as entries:
        for entry in entries:
            name, ext = os.path.splitext(entry.name)
            if ext not in ['.jsonl', '.json']:
                continue

            target_dir = os.path.join(TARGET, name)
            cat2folder[name] = target_dir
            os.makedirs(target_dir, exist_ok=True)

def clas_photos():
    init()
    with os.scandir(SOURCE) as entries:
        for entry in tqdm(entries, ncols='100', desc='num'):
            if not entry.is_dir():
                continue

            photo_path = None
            json_path = None

            with os.scandir(entry.path) as sentries:
                for sentry in sentries:
                    ext = os.path.splitext(sentry.name)[1].lower()
                    if ext in ['.png', '.jpg']:
                        photo_path = sentry.path
                    elif ext in ['.json', '.jsonl']:
                        json_path = sentry.path
            
            if photo_path and json_path:
                with open(json_path, 'r', encoding='utf-8') as f:
                    if json_path.endswith('.jsonl'):
                        data = json.loads(f.readline()) 
                    else:
                        data = json.load(f)
                
                category = data.get('category')
                
                if category and category in cat2folder:
                    new_file_name = f"{entry.name}_{os.path.basename(photo_path)}"
                    target_file_path = os.path.join(cat2folder[category], new_file_name)
                    
                    shutil.copy(photo_path, target_file_path)
                else:
                    print(f"跳过: {entry.name} - 找不到对应分类 '{category}'")

if __name__ == '__main__':
    clas_photos()
    print("分类提取完成！")