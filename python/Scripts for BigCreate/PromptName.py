import os
from pathlib import Path
from tqdm import tqdm

DANXIA = r"E:\WorkSpace\Data\dataset\Danxia\outputs"
KARST = r"E:\WorkSpace\Data\dataset\Karst\Karst"
LOESS = r"E:\WorkSpace\Data\dataset\Huangtu\Huangtu"
ICE = r"E:\WorkSpace\Data\dataset\IceMountain\IceMountain"
DESERT = r"E:\WorkSpace\Data\dataset\desert\desert"
YARDANG = r"E:\WorkSpace\Data\dataset\Yadan\Yadan"
INPUT = r"E:\WorkSpace\Data\unet_test\txt"

danxia = set()
karst = set()
loess = set()
ice = set()
desert = set()
yardang = set()

def extract_name(terrain_set: set, dir_path: str):
    dirs = Path(dir_path)

    for dir in dirs.iterdir():
        terrain_set.add(dir.name)


def init():
    extract_name(danxia, DANXIA)
    extract_name(karst, KARST)
    extract_name(ice, ICE)
    extract_name(desert, DESERT)
    extract_name(yardang, YARDANG)
    extract_name(loess, LOESS)

def main():
    init()

    files = [f for f in Path(INPUT).iterdir()]


    for file in tqdm(files, desc='writing file'):
        name = file.stem
        category = "general"

        if name in danxia: category = "danxia"
        elif name in karst: category = "karst"
        elif name in ice: category = "ice mountain"
        elif name in desert: category = "desert"
        elif name in yardang: category = "yardang"
        else: category = "loess"

        with open(file, "r", encoding="utf-8") as f:
            cont = f.read()

        for i in range(len(cont)):
            if cont[i] == ';':
                cont = cont[i + 2: ]
                break

        prefix = f"This is a terrain named {category}; "

        file.write_text(prefix + cont, encoding='utf-8')

if __name__ == '__main__':
    main()