# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 18:48:35 2017

@author: chenwen
"""
#使用urllib和BeautifulSoup
from urllib.request import urlopen
from bs4 import BeautifulSoup

#将网页读取并转化为BeautifulSoup对象
html = urlopen("http://www.shibor.org/shibor/web/html/shibor.html")

bsObj = BeautifulSoup(html, "lxml")

#根据标签属性提取相应信息
time_tag = bsObj.find_all("td",{"class":"infoTitleW"})
time = time_tag[0].get_text().replace("\xa0\xa0","")

table = bsObj.body.find_all("table",{"class":"shiborquxian"})
tds = table[0].find_all("td", {"width":"30%"})
td_list = list()
for td in tds:
    item = td.get_text()
    item = item.replace("\xa0\xa0","")
    td_list.append(item)


#输出    
title = ["O/N","1W", "2W", "1M", "3M", "6M", "9M", "1Y"]
print(time)
print("期限\tShibor(%)\t涨跌(BP)")
for i in range(8):
    print(title[i] + '\t' + td_list[i * 2] + '\t' + td_list[i * 2 + 1])