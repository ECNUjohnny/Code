import requests
from bs4 import BeautifulSoup
import urllib.parse

def extract_landform_locations(landform_name):
    """
    从中文维基百科提取特定地貌的分布地点
    """
    print(f"正在搜索[{landform_name}]的维基百科页面...\n" + "-"*40)
    
    # 1. 构造维基百科的 URL (处理中文 URL 编码)
    base_url = "https://zh.wikipedia.org/wiki/"
    # 维基百科有时会自动重定向，这里我们直接请求
    url = base_url + urllib.parse.quote(landform_name)
    
    # 2. 设置请求头（非常重要，伪装成浏览器，防止被维基百科拦截）
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # 如果页面不存在，维基百科通常返回 404
        if response.status_code == 404:
            print(f"未找到关于“{landform_name}”的页面，请检查名称是否准确。")
            return
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"网络请求失败: {e}")
        return

    # 3. 解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 4. 定义我们要寻找的章节关键词
    target_keywords = ['著名景点', '分布', '代表', '著名', '实例', '名胜', '地理', '主要']
    
    found_locations = []
    
    # 获取页面正文部分
    content_div = soup.find('div', id='mw-content-text')
    
    if not content_div:
        print("无法解析页面正文。")
        return

    # 遍历所有的标题标签 (h2, h3)
    headers = content_div.find_all(['h2', 'h3'])
    
    for header in headers:
        headline = header.find('span', class_='mw-headline')
        if not headline:
            continue
            
        heading_text = headline.get_text()
        
        # 如果标题包含我们的关键词（例如："中国丹霞分布", "世界分布"）
        if any(keyword in heading_text for keyword in target_keywords):
            print(f"\n>> 找到相关章节: 【{heading_text}】")
            
            # 查找该标题后面的兄弟节点，直到遇到下一个相同或更高级别的标题
            sibling = header.find_next_sibling()
            while sibling and sibling.name not in ['h2', 'h3']:
                # 提取段落 <p> 和列表 <ul>/<li> 中的内容
                if sibling.name in ['p', 'ul', 'ol']:
                    # 提取纯文本
                    text = sibling.get_text(strip=True)
                    if text:
                        print(f"  - 文本内容: {text[:100]}..." if len(text) > 100 else f"  - 文本内容: {text}")
                    
                    # 进阶提取：提取这一段中带链接的名词（这些通常是具体的地点、山脉、国家）
                    links = sibling.find_all('a')
                    for link in links:
                        # 排除带有特定前缀的系统链接 (如 Wiki:, Help:) 和注脚 ([1])
                        href = link.get('href', '')
                        title = link.get('title', '')
                        if href.startswith('/wiki/') and ':' not in href and title:
                            found_locations.append(title)
                            print(f"    -> 提取到潜在地点/实体: {title}")
                            
                sibling = sibling.find_next_sibling()

    print("\n" + "="*40)
    # 去重并展示结果
    unique_locations = list(set(found_locations))
    print(f"提取完成！共找到 {len(unique_locations)} 个带有专属百科页面的潜在地点/实体。")
    # 可以选择打印出前 20 个
    print(unique_locations[:20])
    
    return unique_locations


# ==========================================
# 运行测试
# ==========================================
if __name__ == "__main__":
    # 你可以把这里换成 "喀斯特地貌", "黄土地貌", "冰川地貌" 等
    target_landform = "丹霞地貌" 
    extract_landform_locations(target_landform)