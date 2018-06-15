# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 16:43:32 2018

@author: chenw
"""

import re

def string_to_list1(string, length):
    string_list = list()
    while len(string) > length:
        string_list.append(string[:length])
        string = string[length:]
    else:
        string_list.append(string)
    return string_list

def string_to_list2(string, length): 
    string_list = re.findall('.{' + str(length) + '}', string)
    string_list.append(string[(len(string_list) * length):])
    return string_list

def string_to_list3(string, length):
    return [string[x: x + length] for x in range(0, len(string), length)]

def string_to_generator(string, length):
    return (string[x: x + length] for x in range(0, len(string), length))