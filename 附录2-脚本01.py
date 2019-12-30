from bs4 import BeautifulSoup
import requests
# 打开一个网页，请修改url中的xxxxxx
url = "https://space.bilibili.com/xxxxxxx/"
headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
page = requests.get(url,headers=headers)
page_content = page.content
# 使用BeautifulSoup库解析网页
soup = BeautifulSoup(page_content, "lxml")
content = soup.find("div", class_="n-statistics")
print(content)