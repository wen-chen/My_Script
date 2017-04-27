# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 10:50:00 2017

@author: chenw
"""

import requests
from requests.exceptions import RequestException
import re

def get_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

#this function is unfinished
somethins = ''
def parse_html(html):
    pattern = re.compile(somethins)
    items = re.findall(pattern, html)
    for item in items:
        yield somethins