# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 20:34:12 2017

@author: chenwen
"""

import sys, getopt

opts, args = getopt.getopt(sys.argv[1:], "hi:")
for op, value in opts:
    if op == "-i":
        infilename = value
    elif op == "-h":
        print("Usage: python3 stat_fa_len.py -i in.fa")
        sys.exit()

i = -1
len_list = []
with open(infilename, "r") as infile:
    for line in infile:
        line = line.strip()
        if line[0] == '>':
            i = i + 1
            len_list.append(0)
        else:
            len_list[i] = len_list[i] + len(line)

len_value = len(len_list)
max_value = max(len_list)
min_value = min(len_list)
average_value =sum(len_list) // len_value
len_list.sort()
Upper_value = len_list[int(len_value * 0.25)]
median_value = len_list[int(len_value * 0.5)]  
Lower_value = len_list[int(len_value * 0.75)]

print("Sequece Number: " + str(len_value))   
print("Max sequece length: " + str(max_value))
print("Min sequece length: " + str(min_value))
print("Average sequece length: " + str(average_value))
print("25% sequece length < " + str(Upper_value))
print("Median sequece length: " + str(median_value))
print("25% sequece length > " + str(Lower_value))        

            