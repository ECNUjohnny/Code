import os
from pathlib import Path
from tqdm import tqdm

DANXIA = r"E:\WorkSpace\Data\dataset\Danxia\outputs"
KARST = r"E:\WorkSpace\Data\dataset\Karst\Karst"
LOESS = r"E:\WorkSpace\Data\dataset\Huangtu\Huangtu"
ICE = r"E:\WorkSpace\Data\dataset\IceMountain\IceMountain"
DESERT = r"E:\WorkSpace\Data\dataset\desert\desert"
YARDANG = r"E:\WorkSpace\Data\dataset\Yadan\Yadan"
INPUT = r"E:\WorkSpace\Data\unet\txt"

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

    files = Path(INPUT)

    for file in tqdm(files.iterdir(), desc='writing file'):
        name = file.stem
        catagory = "general"

        if name in danxia: catagory = "danxia"
        elif name in karst: catagory = "karst"
        elif name in ice: catagory = "ice mountain"
        elif name in desert: catagory = "desert"
        elif name in yardang: catagory = "yardang"
        elif name in loess: catagory = "loess"

        with open(file, "r", encoding="utf-8") as f:
            cont = f.read()

        for i in range(len(cont)):
            if cont[i] == ';':
                cont = cont[i + 2: ]
                break

        prefix = f"This is a terrain named {catagory}; "

        file.write_text(prefix + cont, encoding='utf-8')

if __name__ == '__main__':
    main()