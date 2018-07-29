# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 11:31:25 2018

@author: chenw
"""


import sys, getopt

opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
for op, value in opts:
    if op == "-i":
        BED4_File_name = value
    elif op == "-o":
        BED12_File_Name = value
    elif op == "-h":
        print("Usage: python3 BED4_to_BED12.py -i BED4.bed -o BED12.bed")
        sys.exit()
        

def bed4list_to_bed12_list(bed4list):
    start = bed4list[1]
    end = bed4list[2]
    size = str(int(end) - int(start))
    bed4list.extend(['0', '+', start, end, '0,0,0', '1', 
                                 size + ',', '0,'])
    return bed4list


BED4_File = open(BED4_File_name, 'r')
BED12_File = open(BED12_File_Name, 'w')

for line in BED4_File:
    bed4list = line.strip().split('\t')
    bed12list = bed4list_to_bed12_list(bed4list)
    line = '\t'.join(bed12list) + '\n'
    BED12_File.write(line)

BED4_File.close()
BED12_File.close()

