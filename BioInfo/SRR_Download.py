# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 16:54:10 2017

@author: chenwen
"""

import sys, getopt, os

opts, args = getopt.getopt(sys.argv[1:], "hi:")
for op, value in opts:
    if op == "-i":
        SRR = value
    elif op == "-h":
        print("Usage: python3 SRR_Download.py -i SRR_Number")
        sys.exit()

constant = "wget -c ftp://ftp-trace.ncbi.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/"
variable = SRR[:6] + '/' + SRR + '/' + SRR + ".sra"
cmd = constant + variable
os.system(cmd)