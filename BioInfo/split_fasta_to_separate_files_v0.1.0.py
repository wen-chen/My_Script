# -*- coding: utf-8 -*-
"""
Created on Tue May 29 03:02:13 2018

@author: chenw
"""

import getopt, sys, os

usage = "split_fasta_to_separate_files.py -i input.fa -o output_dir"

opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
fa_in_file = ""
fa_out_dir = ""
for op, value in opts:
    if op == "-i":
        fa_in_file = value
    elif op == "-o":
        fa_out_dir = value      
    elif op == "-h":
        print(usage)
        sys.exit()
        
if not os.path.exists(fa_out_dir):      
    os.makedirs(fa_out_dir)
        
n = -1
outfiles = list()
with open(fa_in_file, 'r') as fa_in:
    for line in fa_in:
        if line[0] == '>':
            if n > -1:
                outfiles[n].close()
            n = n + 1
            name = line.strip()[1:]
            fa_out = open(fa_out_dir + '/' + name + '.fa', 'w')
            fa_out.write(line)
            outfiles.append(fa_out)
        else:            
            outfiles[n].write(line)

outfiles[n].close()
        