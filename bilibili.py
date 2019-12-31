# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 10:12:07 2019

@author: 徐柳青
@Email:45045590@qq.com
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException 
from selenium.common.exceptions import StaleElementReferenceException 
from selenium.common.exceptions import ElementNotInteractableException
import time
import re
import pandas as pd
import sqlite3
from bs4 import BeautifulSoup
import random
import requests
import json

def get_Summary(Id):
    browser.get(base_url+str(Id))
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(2)
    #获取网页的HTML代码
    html=browser.page_source
    #使用BeautifulSoup进行解析
    soup=BeautifulSoup(html,'lxml')
    #查找包含统计信息的部分
    nstatistics = soup.find("div",class_="n-statistics")
    #获取统计信息，创建一个新词典
    try:
        播主名称 = soup.find("span",id="h-name").string
        stat_Info = {'mid':[Id],'播主名称':[播主名称]}
        #创建一个re正则搜索规则
        parse_number = re.compile(r'\d*')
        for type_tag in ["a","div"]:
            for i in nstatistics.find_all(type_tag):
                name = i.p.string
                number_str =parse_number.findall(i.get("title"))
                #print(name,':',int("".join(number_str)))
                stat_Info[name] = int("".join(number_str))
        for i in ['关注数', '粉丝数', '获赞数', '播放数', '阅读数']:
            if i not in stat_Info.keys():
                stat_Info[i] = [None]
        #获取播主主页空间中的内容
        space = soup.find('div',class_="s-space")
        #获取上传的视频数/相册数
        try: 
            stat_Info['视频数'] = [int(space.find('div',class_="section video full-rows").h3.span.string)]
        except AttributeError:
            stat_Info['视频数'] = [None]
        try: 
            stat_Info['相册数'] = [int(space.find('div',class_="section album").span.string)]
        except AttributeError:
            stat_Info['相册数'] = [None]
        stat_Info['等级'] =  [int(soup.find('a',class_="h-level m-level").get('lvl'))]
        if '年度大会员' == soup.find('a',class_="h-vipType").string:
            stat_Info['年度大会员'] = [1]
        else:
            stat_Info['年度大会员'] = [0]
        #return stat_Info
    except AttributeError:
        stat_Info = {'mid':[Id],'播主名称':["不存在"],
                     '关注数':[None],'粉丝数':[None],'获赞数':[None],
                     '播放数':[None],'视频数':[None],'相册数':[None],
                     '等级':[None],'年度大会员':[None]}
    return stat_Info

def get_Concerns(Id):
    #获取关注的信息
    browser.get(base_url+str(Id)+tail_url['关注'])
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    names = []
    IDs = []
    TAGs = []
    VIPs = []
    next_Page = True
    while next_Page:
        try:
            time.sleep(1)
            names_Xpath = browser.find_elements_by_xpath('/html/body/div[2]/div[4]/div/div/div/div[2]/div[2]/div[2]/ul[@class="relation-list"]/li[@class="list-item clearfix"]/div[@class="content"]/a/span')
            urls_Xpath = browser.find_elements_by_xpath('//div[@class="follow-main"]//ul[@class="relation-list"]//li[@class="list-item clearfix"]//a[@class="cover"]')
            tags_Xpath = browser.find_elements_by_xpath('/html/body/div[@id="app" and @class="visitor"]//div[@class="follow-main"]//ul[@class="relation-list"]/li[@class="list-item clearfix"]//div[@class="content"]/p')
            for i in range(len(tags_Xpath)):
                names.append(names_Xpath[i].text)
                IDs.append(urls_Xpath[i].get_attribute('href').split('/')[-2])
                TAGs.append(tags_Xpath[i].text)
                if 'this-is-vip' in names_Xpath[i].get_attribute('class'):
                    VIPs.append(1)
                else:
                    VIPs.append(0)
            #先点击后判断5页限制
            browser.find_element_by_link_text('下一页').click()
            #5页限制
            get_Next = browser.find_elements_by_xpath('//div[contains(@class,"modal-container") and contains(@class,"prohibit-modal")]')[0].get_attribute('style')
            if 'none' in get_Next:
                next_Page = True
            else:
                next_Page = False
        except NoSuchElementException:
            next_Page = False
    if len(names) == len(IDs) == len (TAGs):
        return {'IDs':IDs,'名称': names ,'mid':[Id]*len(names),'TAG':TAGs,'VIP':VIPs}
    else:
        print("B站可能已经改变规则，请认真核对！！！")


def get_Fans(Id):
    #获取粉丝的信息
    browser.get(base_url+str(Id)+tail_url['粉丝'])
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    names = []
    IDs = []
    TAGs = []
    next_Page = True
    while next_Page:
        try:
            time.sleep(1)
            names_Xpath = browser.find_elements_by_xpath('/html/body/div[2]/div[4]/div/div/div/div[2]/div[2]/div[2]/ul[@class="relation-list"]/li[@class="list-item clearfix"]/div[@class="content"]/a/span')
            urls_Xpath = browser.find_elements_by_xpath('//div[@class="follow-main"]//ul[@class="relation-list"]//li[@class="list-item clearfix"]//a[@class="cover"]')
            tags_Xpath = browser.find_elements_by_xpath('/html/body/div[@id="app" and @class="visitor"]//div[@class="follow-main"]//ul[@class="relation-list"]/li[@class="list-item clearfix"]//div[@class="content"]/p')
            for i in range(len(tags_Xpath)):
                names.append(names_Xpath[i].text)
                IDs.append(urls_Xpath[i].get_attribute('href').split('/')[-2])
                TAGs.append(tags_Xpath[i].text)
            #先点击后判断5页限制
            browser.find_element_by_link_text('下一页').click()
            #5页限制
            get_Next = browser.find_elements_by_xpath('//div[contains(@class,"modal-container") and contains(@class,"prohibit-modal")]')[0].get_attribute('style')
            if 'none' in get_Next:
                next_Page = True
            else:
                next_Page = False
        except NoSuchElementException:
            next_Page = False
    if len(names) == len(IDs) == len (TAGs):
        return {'IDs':IDs,'名称': names ,'mid':[Id]*len(names),'TAG':TAGs}
    else:
        print("B站可能已经改变规则，请认真核对！！！")

## 建立数据表
def create_DB(db):
    with sqlite3.connect(db) as conn:
        Summarys = (
        "Create Table If Not Exists Summarys( "
            "mid INTEGER PRIMARY KEY Not NULL, "
            "播主名称 varchar(100), "
            "关注数 INTEGER, "
            "粉丝数 INTEGER, "
            "获赞数 INTEGER, "
            "播放数 INTEGER, "
            "阅读数 INTEGER, "
            "视频数 INTEGER, "
            "相册数 INTEGER, "
            "等级 INTEGER, "
            "年度大会员 INTEGER "
        ")"
        )

        Fans = (
        "Create Table If Not Exists Fans( "
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "IDs INTEGER,"
            "名称 varchar(100), "
            "mid INTEGER, "
            "TAG varchar(100) "
        ")"
        )

        Concerns = (
        "Create Table If Not Exists Concerns( "
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "IDs INTEGER,"
            "名称 varchar(100), "
            "mid INTEGER, "
            "TAG varchar(100), "
            "VIP INTEGER "
        ")"
        )
        cursor = conn.cursor()
        cursor.execute(Summarys)
        cursor.execute(Fans)
        cursor.execute(Concerns)
        cursor.close()
        conn.commit()


def sent_SQL(db):
    with sqlite3.connect(db) as conn:
        pd.DataFrame(Summarys_Info).to_sql('Summarys',conn,if_exists='append',index=False)
        pd.DataFrame(Fans_Dict).to_sql('Fans',conn,if_exists='append',index=False)
        pd.DataFrame(Concerns_Dict).to_sql('Concerns',conn,if_exists='append',index=False)

def randGet_ID(db):
    #获取已经录入的播主mid
    with sqlite3.connect(db) as conn:
        get_E_MID="SELECT * From Summarys"
        exsist_MID = pd.read_sql(con=conn,sql=get_E_MID)['mid']
    Ok = True
    while Ok:
        Id = random.choice(range(80000000))
        if Id in exsist_MID.to_list():
            pass
        else:
            Ok = False
            return Id

if __name__ == '__main__':
    #打开浏览器并预热
    #profile=webdriver.FirefoxOptions()
    #profile.add_argument('-headless') #设置无头模式
    #设置代理服务器
    #profile.set_preference('network.proxy.type', 1)
    #profile.set_preference('network.proxy.http',IP)#IP为你的代理服务器地址:如‘127.0.0.0’，字符串类型
    #profile.set_preference('network.proxy.http_port', PORT)  #PORT为代理服务器端口号:如，9999，整数类型
    #browser = webdriver.Firefox(options=profile)
    browser = webdriver.Firefox()
    browser.maximize_window()
    time.sleep(3)
    #链接数据库
    db = "bilibli.db"
    create_DB(db)
    #基础链接
    base_url = 'https://space.bilibili.com/'
    tail_url = {'关注':'/fans/follow','粉丝':'/fans/fans'}
    headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    #随机数量
    n = 200
    i=0
    while i <= n:
        Id = randGet_ID(db)
        summaries_temp = requests.get('https://api.bilibili.com/x/space/upstat?mid='+ str(Id),headers=headers)
        code = json.loads(summaries_temp.text)["message"]
        if  code != "用户不存在":
            Summarys_Info = get_Summary(Id=Id)
            Fans_Dict = get_Fans(Id=Id)
            Concerns_Dict = get_Concerns(Id=Id)
            sent_SQL(db)
            i += 1
        else:
            pass
    browser.quit()