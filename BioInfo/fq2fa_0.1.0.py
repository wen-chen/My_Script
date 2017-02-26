# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 12:50:03 2016

@author: biochen
"""

import sys, getopt

opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
for op, value in opts:
    if op == "-i":
        FQ_in_File_Name = value
    elif op == "-o":
        FA_in_File_Name = value
    elif op == "-h":
        print("Usage: python3 fq2fa.py -i input.fq -o output.fa")
        sys.exit()
        
fq = open(FQ_in_File_Name, "r")
fa = open(FA_in_File_Name, "w")
i = 1
for line in fq:
    if i%4 == 2:
        fa.write(line)
    i = i + 1
fq.close()
fa.close()