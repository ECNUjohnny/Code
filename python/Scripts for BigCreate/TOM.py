import numpy as np
from PIL import Image

# 读两张不同的原始 PNG
arr1 = np.load(r"E:\WorkSpace\Data\unet\dem\0001_Aletsch_Glacier_U_Valley_Switzerland_DEM_y0_x0_base.npy")
arr2 = np.array(Image.open(r"E:\WorkSpace\Data\dem\0002_Ansai_Hills_Loess_Plateau_Shaanxi_DEM_y0_x1024_base.png"))

print("Map A max:", arr1.max())
print("Map B max:", arr2.max())
print(arr1.min())