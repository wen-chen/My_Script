# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 14:18:47 2018

@author: chenw
"""

import sys, getopt
import re
import requests
from bs4 import BeautifulSoup


usage = '''python3 crawling_KEGG.py -i K_ID.list -o K_info.tsv
-i input K_ID, one id per line
-o output K_info, five columns divided by tab, 'K_id, name, definition, ko_id, pathway'
-e error_log, the default value is 'K_err.tsv', two columns divided by tab, 'K_id, error_type'
-h print usage'''


#==============================================================================
# 获得参数
#==============================================================================
opts, args = getopt.getopt(sys.argv[1:], "hi:o:t:e:")
K_ID_file_name = "K_ID.list"
K_info_file_name = "K_info.tsv"
error_log_file_name = "K_err.tsv"
thread = 1
for op, value in opts:
    if op == "-i":
        K_ID_file_name = value
    elif op == "-o":
        K_info_file_name = value
    elif op == "-e":
        error_log_file_name = value
    elif op == "-t":
        thread = int(value)       
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
# 执行爬取
#==============================================================================
K_set = set()
with open(K_ID_file_name,'r') as K_ID_file:
    for line in K_ID_file:
        K_set.add(line.strip())

error_log_file = open(error_log_file_name, 'w')
K_info_file = open(K_info_file_name, 'w')

i = 0
n = len(K_set)
for K in K_set:
    status, info = getInfo(K)
    if status:
        for item in info:
            K_info_file.write('\t'.join(item) + '\n')
    else:
        error_log_file.write(K + '\t' + info + '\n')
    i = i + 1
    print("\rProgress: {:.2f}%".format(i * 100 / n), end='', flush=True)
print('')

error_log_file.close()
K_info_file