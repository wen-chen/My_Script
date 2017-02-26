# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 19:43:00 2015

@author: biochen
"""

import sys, getopt, csv

# get parameter
opts, args = getopt.getopt(sys.argv[1:], "hi:o:s:")
input_file = ""
output_file = ""
source = ""
for op, value in opts:
    if op == "-i":
        input_file = value
    elif op == "-o":
        output_file = value
    elif op == "-s":
        source = value        
    elif op == "-h":
        print("Usage: python3 BED2GTF.py -i input.bed -o output.gtf -s source")
        sys.exit()


BED_in_file = open(input_file, "r")
GTF_out_file = open(output_file, "w")
BED = csv.reader(BED_in_file, dialect = "excel-tab")
GTF = csv.writer(GTF_out_file, dialect = "excel-tab", quotechar = "'")

for item in BED:
    transcript = []
    transcript.append(item[0])
    transcript.append(source)
    transcript.append("transcript")
    transcript.append(int(item[1]) + 1)
    transcript.append(int(item[2]) + 1)
    transcript.append(item[4])
    transcript.append(item[5])
    transcript.append(".")
    transcript.append('transcript_id "' + item[3] + '";')
    GTF.writerow(transcript)
    exon_number = int(item[9])
    exon_size = list(map(int, (filter(lambda x:x and len(x.strip()) > 0, item[10].split(",")))))
    exon_start = list(map(int, (filter(lambda x:x and len(x.strip()) > 0, item[11].split(",")))))
    for i in range(exon_number):
        exon = []
        exon.append(item[0])
        exon.append(source)
        exon.append("exon")
        exon.append(int(item[1]) + exon_start[i] + 1)
        exon.append(exon[3] + exon_size[i] - 1)
        exon.append(item[4])
        exon.append(item[5])
        exon.append(".")
        exon.append('transcript_id "' + item[3] + '\";')
        GTF.writerow(exon)

BED_in_file.close()
GTF_out_file.close()