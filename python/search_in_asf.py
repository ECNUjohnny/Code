import re

def dms_to_dd(degrees, minutes, seconds, direction):
    """
    将度分秒转换为十进制度 (Decimal Degrees)
    """
    # 核心转换公式
    dd = float(degrees) + float(minutes)/60 + float(seconds)/3600
    
    # 如果是南半球 (S) 或西半球 (W)，数值必须是负数
    if direction in ['S', 'W']:
        dd *= -1
        
    return dd

def convert_to_asf_format(dms_str):
    """
    解析坐标字符串并输出 ASF 兼容格式
    """
    # 使用正则表达式提取数字和方向字母
    # 兼容各种单双引号、特殊符号和空格
    pattern = r"(\d+)[°\s]+(\d+)[′'\s]+(\d+(?:\.\d+)?)[″\"\s]+([NSEW])"
    matches = re.findall(pattern, dms_str.upper())
    
    if len(matches) != 2:
        raise ValueError("无法解析坐标，请检查字符串格式是否类似于 '28°31′47″N 118°33′55″E'")

    lat = None
    lon = None

    # 智能判断经纬度（不依赖前后顺序）
    for match in matches:
        deg, min, sec, direction = match
        dd = dms_to_dd(deg, min, sec, direction)
        
        if direction in ['N', 'S']:
            lat = dd
        elif direction in ['E', 'W']:
            lon = dd
            
    # 保留 6 位小数，这对于卫星影像检索精度已经足够
    lat = round(lat, 6)
    lon = round(lon, 6)
    
    return lat, lon

# === 测试代码 ===
if __name__ == "__main__":
    # 你输入的坐标
    dms_coordinate = "27°39′00″N 117°57′00″E"
    
    try:
        lat, lon = convert_to_asf_format(dms_coordinate)
        
        print(f"原始输入: {dms_coordinate}")
        print("-" * 40)
        print(f"✅ 十进制度纬度 (Lat): {lat}")
        print(f"✅ 十进制度经度 (Lon): {lon}")
        print("-" * 40)
        print("🚀 ASF 检索可用格式:")
        # ASF Vertex 网站搜索栏可直接使用的坐标格式 (Lat, Lon)
        print(f"Vertex 网页搜索框 : {lat},{lon}") 
        # ASF API 中 intersectsWith 参数需要的 WKT 格式 (注意是 Lon Lat)
        print(f"ASF API WKT 格式: POINT({lon} {lat})") 
        
    except Exception as e:
        print(f"错误: {e}")