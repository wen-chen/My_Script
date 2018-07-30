# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 16:40:41 2018

@author: chenw
"""

def find_position_list(sub_string, string):
    position_list = list()
    position = string.find(sub_string)
    while position != -1:
        position_list.append(position)
        position = string.find(sub_string, position + 1)
    return position_list