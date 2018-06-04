# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 00:59:31 2018

@author: chenw
"""

import sys, getopt
import re
import requests
from bs4 import BeautifulSoup
from multiprocessing import Process, Lock, Manager
import time

usage = '''python3 crawling_KEGG.py -i K_ID.list -o K_info.tsv
-i input K_ID, one id per line
-o output K_info, five columns divided by tab, 'K_id, name, definition, ko_id, pathway'
-p process, the default value is 1
-e error_log, the default value is 'K_err.tsv', two columns divided by tab, 'K_id, error_type'
-h print usage
'''


#==============================================================================
# 获得参数
#==============================================================================
opts, args = getopt.getopt(sys.argv[1:], "hi:o:p:e:")
K_ID_file_name = "K_ID.list"
K_info_file_name = "K_info.tsv"
error_log_file_name = "K_err.tsv"
process_num = 1
for op, value in opts:
    if op == "-i":
        K_ID_file_name = value
    elif op == "-o":
        K_info_file_name = value
    elif op == "-e":
        error_log_file_name = value
    elif op == "-p":
        process_num = int(value)       
    elif op == "-h":
        print(usage)
        sys.exit()


#==============================================================================
# 爬取网页
#==============================================================================
def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        #r.encoding = r.apparent_encoding
        return r.text
    except:
        return 0   


def getInfo(keyword):
    url = 'http://www.genome.jp/dbget-bin/www_bget?ko:{}'.format(keyword)
    html = getHTMLText(url)
    if html:
        info = list()
        name_pattern = re.compile('overflow-y\:hidden">([0-9a-zA-Z]+)<')
        definition_pattern = re.compile('overflow-y\:hidden">([0-9a-zA-Z\s?]+) \[EC')
        try:
            soup = BeautifulSoup(html, "html.parser")
            name = soup.body.find_all('td', {"class":"td41"})[0].text.strip()
            definition = soup.body.find_all('td', {"class":"td40"})[1].text.strip()
            pathway_table = soup.body.find_all('td', {"class":"td41"})[1]
            for item in pathway_table.find_all('tr'):
                ko_tag, pathway_tag = item.find_all('td')
                ko = ko_tag.text.strip()
                pathway = pathway_tag.text.strip()
                if 'ko' in ko:
                    info.append([keyword, name, definition, ko, pathway])
            if info:
                return (1, info)
            else:
                error_type = "K_id not included in a pathway"
                return (0, error_type)                
        except:
            error_type = "Parse HTML Text Failed!"
            return (0, error_type)
    else:
        error_type = "Get HTML Text Failed!"
        return (0, error_type)

#==============================================================================
# 定义进程函数，锁，通信变量
#==============================================================================
manager = Manager()
K_dict = manager.dict()
lock = Lock()

def task(process_i, process_num, K_num, K_list, lock):
    K_process_dict = dict()
    global K_dict
    for i in range(int(process_i / process_num * K_num), int((process_i + 1) / process_num * K_num)):
        K = K_list[i]
        info = getInfo(K)
        K_process_dict[K] = info
        if i % 100:
            with lock:
                K_dict.update(K_process_dict)
    with lock:
        K_dict.update(K_process_dict)
     

#==============================================================================
# 执行多线程爬取
#==============================================================================
K_set = set()
with open(K_ID_file_name,'r') as K_ID_file:
    for line in K_ID_file:
        K_set.add(line.strip())        

K_list = list(K_set)
K_num = len(K_list)

process_list = []
for process_i in range(process_num):
    process_list.append(Process(target=task, args=(process_i, process_num, K_num, K_list, lock )))
for process in process_list:
    process.start()

done_num = len(K_dict)
while (done_num < K_num):
    done_num = len(K_dict)
    print("\r当前进度: {:.2f}%".format(done_num * 100 / K_num), end='', flush=True)
    time.sleep(30)
print("\r当前进度: {:.2f}%".format(done_num * 100 / K_num), end='\n', flush=True)

error_log_file = open(error_log_file_name, 'w')
K_info_file = open(K_info_file_name, 'w')

K_dict = dict(K_dict)
for K in K_dict:
    status, info = K_dict[K]
    if status:
        for item in info:
            K_info_file.write('\t'.join(item) + '\n')
    else:
        error_log_file.write(K + '\t' + info + '\n')
        
error_log_file.close()
K_info_file