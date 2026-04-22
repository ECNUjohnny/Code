import requests
import json

def get_bbox(name, out_file):
    url = "https://nominatim.openstreetmap.org/search"
    p = {'q': name, 'format': 'json', 'limit': 1}
    h = {'User-Agent': 'gis-fetcher'} 
    
    try:
        req = requests.get(url, params=p, headers=h)
        data = req.json()
        
        if not data:
            print(f"未找到: {name}")
            return
            
        # bbox 格式为: [南纬, 北纬, 西经, 东经]
        box = data[0]['boundingbox']
        
        res = {
            "name": name,
            "bbox": [float(box[0]), float(box[1]), float(box[2]), float(box[3])]
        }
        
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
            
        print(f"✅ 成功! {name} 范围: {res['bbox']}")
        
    except Exception as e:
        print(f"❌ 报错: {e}")

# 运行测试
q = "丹霞山"
f = "./Data/baota.json"
get_bbox(q, f)