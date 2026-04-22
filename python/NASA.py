import earthaccess
import os

# 1. 登录授权 (极其重要)
# 第一次运行会提示你输入 Earthdata 的 Username 和 Password
# 它会自动帮你保存凭证，下次就不用再输了
auth = earthaccess.login(strategy="interactive")

# 2. 定义你要搜索的数据和范围
# short_name: "NASADEM_HGT" 就是 30米高程数据的官方简称
# bounding_box: (最小经度, 最小纬度, 最大经度, 最大纬度) -> 丹霞山范围
bbox = (113.607, 24.863, 113.798, 25.070)

print("正在通过 NASA API 检索数据...")
results = earthaccess.search_data(
    short_name="NASADEM_HGT",
    bounding_box=bbox,
    count=4  # 最大返回数量（防止你不小心框了整个地球导致崩溃）
)

print(f"找到了 {len(results)} 个匹配的数据瓦片！")

# 3. 执行批量下载
# 定义你要把数据存在电脑的哪个文件夹
download_dir = "D:/File"
os.makedirs(download_dir, exist_ok=True)

print("开始多线程下载...")
# 这一句会自动处理所有的网络请求、断点续传和多线程并发
downloaded_files = earthaccess.download(results, local_path=download_dir)

print("全部下载完成！文件路径：")
for file in downloaded_files:
    print(file)