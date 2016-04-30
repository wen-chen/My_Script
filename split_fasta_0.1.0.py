# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 23:44:41 2015

@author: biochen
"""
import sys, getopt

# get parameter
opts, args = getopt.getopt(sys.argv[1:], "hi:o:x:")
X = 1
input_file = ""
prefix = "split_"
for op, value in opts:
    if op == "-i":
        input_file = value
    elif op == "-o":
         prefix = value
    elif op == "-x":
        X = int(value)
    elif op == "-h":
        print("Usage: python3 split_fasta.py -i input.fasta -o prefix -x split_number")
        print("default prefix = split_")
        print("default split_number = 1")
        sys.exit()
        
FA_in_file = open(input_file, "r")

# read fasta file to a list
fa_Info = []
fa_Seq = []
fa_Num = -1
for Y in FA_in_file.readlines():
    Y = Y.rstrip()
    if Y[0] == ">":
        fa_Info.append(Y)
        fa_Num = fa_Num + 1
        fa_Seq.append("")
    else:
        fa_Seq[fa_Num] = fa_Seq[fa_Num] + Y

# split the fasta list to multipe files
file_Num = (fa_Num + 1)//X + 1
for i in range(file_Num):
    exec(prefix + str(i + 1) + ' = open("' + prefix + str(i + 1) + '.fasta"' + ', "w")')
    start = i * X
    end = (i + 1) * X
    if end > fa_Num + 1:
        end = fa_Num + 1
    for j in range(start, end, 1):
        exec(prefix + str(i + 1) + '.write(fa_Info[j] + "\\n")')
        while len(fa_Seq[j]) > 60:
            exec(prefix + str(i + 1) + '.write(fa_Seq[j][:60] + "\\n")')
            fa_Seq[j] = fa_Seq[j][60:]
        else:
            exec(prefix + str(i + 1) + '.write(fa_Seq[j] + "\\n")')
    exec(prefix + str(i + 1) + '.close()')

FA_in_file.close()