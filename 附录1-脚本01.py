import requests
import json
import csv
import random
import time

url_Lists = ['https://api.bilibili.com/x/relation/stat?vmid=',
			'https://api.bilibili.com/x/space/navnum?mid=',
			'https://api.bilibili.com/x/space/upstat?mid=']
headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}


def getBiLi_Data(url_Lists,Id,headers=headers):
	#注释用户的统计信息
	summaries_data = {}
	for url in url_Lists:
		URL = url + str(Id)
		summaries_info = requests.get(URL,headers=headers)
		summaries_idict = json.loads(summaries_info.text)
		for k,v in summaries_idict["data"].items():
			#print(k,v)
			summaries_data[k] = v
	return summaries_data

def Panel_Data(datA):
	#该函数仅是对回去到的字典数据进行处理
	new_datA={}
	for k1,v1 in datA.items():
		#print(k1,v1)
		if type(v1) != type({}):
			new_datA[k1] = v1
		else:
			for k2,v2 in v1.items():
				new_datA[str(k1)+'_'+str(k2)] = v2
	return new_datA


def randGet_Data(n,outFile='bili_up.csv'):
	i = 1
	Ids = []
	with open(outFile,"w") as csv_file:
		csv_writer = csv.writer(csv_file)
		csv_writer.writerow(['mid', 'following', 'whisper', 'black',
							 'follower', 'video', 'bangumi', 'cinema',
							 'channel_master', 'channel_guest', 'favourite_master',
							 'favourite_guest', 'tag', 'article_view',
							 'playlist', 'album', 'audio', 'pugv', 
							 'archive_view', 'likes'])
		while i <= n :
			time.sleep(1)
			Id = str(random.random())[8:-1]
			summaries_temp = requests.get('https://api.bilibili.com/x/space/upstat?mid='+ Id,headers=headers)
			if Id not in Ids and json.loads(summaries_temp.text)["code"] != 40061:
				Ids.append(Id)
				i += 1
				datA = getBiLi_Data(url_Lists,Id)
				new_datA = Panel_Data(datA)
				csv_writer.writerow(list(new_datA.values()))


if __name__ == '__main__':
	randGet_Data(20)