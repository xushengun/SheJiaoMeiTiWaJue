#导入需要的库
from bs4 import BeautifulSoup
from selenium import webdriver
import re
#开启浏览器
browser = webdriver.Firefox()
#输入想要获取的网址url，请更换Id中的xxxxxx
Id = xxxxxxx
base_url = 'https://space.bilibili.com/'
browser.get(base_url+str(Id))
#获取网页的HTML代码
html=browser.page_source
#使用BeautifulSoup进行解析
soup=BeautifulSoup(html,'lxml')

#查找包含统计信息的部分
nstatistics = soup.find("div",class_="n-statistics")
#获取统计信息，创建一个新词典，并预置一些不会改变的信息
stat_Info = {'id':Id,'播主名称':soup.find("span",id="h-name").string}
#创建一个re正则搜索规则
parse_number = re.compile(r'\d*')
for type_tag in ["a","div"]:
	for i in nstatistics.find_all(type_tag):
		name = i.p.string
		number_str =parse_number.findall(i.get("title"))
		#print(name,':',int("".join(number_str)))
		stat_Info[name] = int("".join(number_str))
print(stat_Info)

#获取播主主页空间中的内容
space = soup.find('div',class_="s-space")
#获取上传的视频数/相册数
stat_Info['视频数'] = int(space.find('span').string)
stat_Info['相册数'] = int(space.find('div',class_="section album").span.string)

#获取播主空间中最近的25个视频信息
video_info = {}
k=0
for i in space.find_all('a',class_="cover",target="_blank"):
	k += 1 
	video_info['视频_'+str(k)+'_网址'] = 'https://'+"/".join(i.get('href').strip('//').split('/')[:-1])+'/xxxxxxx'
	video_info['视频_'+str(k)+'_名称'] = i.img.get('alt')
	video_info['视频_'+str(k)+'_时长'] = i.span.string
	video_info['视频_'+str(k)+'_上传时间'] = space.find_all('span',class_="time")[k-1].text.strip()
	video_info['视频_'+str(k)+'_播放量'] = space.find_all('span',class_="play")[k-1].text.strip()


###
至此，已经有了stat_Info和video_info两个字典，
如何合并这两个字典以及如何写如csv文件。
作为读者的练习题，留给读者自己完成。
###

#合并字典，提示stat_Info和video_info








#写如csv文件，提示import csv