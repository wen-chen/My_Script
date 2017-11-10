# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 15:56:49 2017

@author: chenw
"""

import sys, getopt

# get parameter
opts, args = getopt.getopt(sys.argv[1:], "hf:q:")
FA_FILE = ""
QUERY = ""
for op, value in opts:
    if op == "-f":
        FA_FILE = value
    elif op == "-q":
        QUERY = value   
    elif op == "-h":
        print("Usage: python3 extract_seq_from_fa.py -f seq.fa -q query")
        sys.exit()

def fafile_2_seq_dict(FileName):
    name_list = list()
    sequence_list = list()
    i = -1
    with open(FileName, "r") as infile:
        for line in infile:
            line = line.strip()
            if line[0] == '>':
                name = line[1:]
                name_list.append(name)
                sequence_list.append(list())
                i = i + 1
            else:
                line = line.upper()
                sequence_list[i].append(line)
    sequence_dict = dict()
    for i in range(len(name_list)):
        sequence_dict[name_list[i]] = ''.join(sequence_list[i])
    return sequence_dict

seq_dict = fafile_2_seq_dict(FA_FILE)

for name,seq in seq_dict.items():
    if QUERY in name:
        print(">" + name)
        while len(seq) > 60:
            print(seq[:60])
            seq = seq[60:]
        else:
            print(seq[:60])