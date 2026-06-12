import shutil
from PIL import Image
from pathlib import Path
from tqdm import tqdm

DANXIA = r"E:\WorkSpace\Data\dataset\Danxia\outputs"
KARST = r"E:\WorkSpace\Data\dataset\Karst\Karst"
LOESS = r"E:\WorkSpace\Data\dataset\Huangtu\Huangtu"
ICE = r"E:\WorkSpace\Data\dataset\IceMountain\IceMountain"
DESERT = r"E:\WorkSpace\Data\dataset\desert\desert"
YARDANG = r"E:\WorkSpace\Data\dataset\Yadan\Yadan"
OUTPUT = r"E:\WorkSpace\Data\unet_test\dem"



def copy_dem(input):
    input_dir = Path(input)
    output_dir = Path(OUTPUT)

    dirs = [d for d in input_dir.iterdir() if d.is_dir()]

    for dir in tqdm(dirs, desc='copying', ncols=100):
        for file in Path(dir).iterdir():
            if file.suffix.lower() == '.png':
                shutil.copy2(file, output_dir / f'{dir.name}.png')


if __name__ == '__main__':
    copy_dem(DANXIA)
    copy_dem(KARST)
    copy_dem(LOESS)
    copy_dem(ICE)
    copy_dem(DESERT)
    copy_dem(YARDANG)