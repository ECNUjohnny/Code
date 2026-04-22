from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def search_arxiv(q_str):
    print("正在启动浏览器...")
    driver = webdriver.Chrome()
    #driver = webdriver.Edge()
    
    try:
        # 1. 访问 arXiv 主页
        driver.get("https://arxiv.org/")
        print("已打开 arXiv 主页")
        
        # 2. 定位搜索框
        # 经过用 F12 开发者工具检查，arXiv 主页的搜索框 name 属性是 "query"
        box = driver.find_element(By.NAME, "query")
        
        # 3. 模拟输入并回车
        print(f"正在输入搜索词: {q_str}")
        box.send_keys(q_str)
        time.sleep(1) 
        box.send_keys(Keys.RETURN)
        
        # 4. 等待网页加载结果
        time.sleep(3) 
        
        # 5. 提取数据
        # arXiv 搜索结果的标题都被放在了 class 为 "title" 的 <p> 标签里
        titles = driver.find_elements(By.CSS_SELECTOR, "p.title")
        
        if titles:
            print(f"\n✅ 成功！为你找到的前 3 篇相关论文：")
            # 只取前 3 个结果打印出来
            for i, t in enumerate(titles[:3]):
                # arXiv 的标题文本通常自带一个 "Title: " 前缀，我们用 replace 把它清洗掉
                clean_title = t.text.replace('Title:', '').strip()
                print(f"{i+1}. {clean_title}")
        else:
            print("\n没有找到结果。")
            
    except Exception as e:
        print(f"❌ 运行报错: {e}")
        
    finally:
        print("\n3秒后自动关闭浏览器...")
        time.sleep(30)
        driver.quit()

if __name__ == "__main__":
    # 我们用你之前关心的地形和机器学习作为测试词
    q = "machine learning DEM"
    search_arxiv(q)