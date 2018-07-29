# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 12:50:03 2016

@author: biochen
"""

import sys, getopt

opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
for op, value in opts:
    if op == "-i":
        FASTQ_File_Name = value
    elif op == "-o":
        FASTA_File_Name = value
    elif op == "-h":
        print("Usage: python3 fq2fa.py -i input.fq -o output.fa")
        sys.exit()
        
FASTQ_File = open(FASTQ_File_Name, "r")
FASTA_File = open(FASTA_File_Name, "w")

i = 1
for line in FASTQ_File:
    if i % 4 == 1:
        line = line.replace("@", ">")
        FASTA_File.write(line)
    elif i % 4 == 2:
        FASTA_File.write(line)
    i = i + 1
    
FASTQ_File.close()
FASTA_File.close()