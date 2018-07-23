# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 11:03:05 2015

@author: biochen
"""

import sys, getopt, re

opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
for op, value in opts:
    if op == "-i":
        GTF_File_Name = value
    elif op == "-o":
        BED_File_Name = value
    elif op == "-h":
        print("Usage: python3 GTF2BED.py -i input.gtf -o output.bed")
        sys.exit()


transcript_dict = dict()
with open(GTF_File_Name, 'r') as GTF_file:
    for line in GTF_file:
        chrom, source, biotype, start, end, score, strand, phase, attributes = line.strip().split('\t')
        if biotype == "exon":
            #通过正则表达式获得转录本ID，如果GTF文件中的转录本ID格式不是transcript_id "ENST00000450305.2"，需要修改正则表达式
            transcript_id = re.findall('transcript_id "([^;]*)"', attributes)[0]       
            if transcript_id in transcript_dict:
                transcript_dict[transcript_id][4].append([int(start), int(end)])
            else:
            # [chrom, score, strand, [[exon_start, exon_end], [...]] ]
                transcript_dict[transcript_id] = [chrom, score, strand, 
                                                  transcript_id, [[int(start), int(end)]]]
            
with open(BED_File_Name, 'w') as BED_File:
    for transcript_id in transcript_dict:
        chrom = transcript_dict[transcript_id][0]
        exon_list = transcript_dict[transcript_id][4]
        exon_list.sort()
        start = str(exon_list[0][0] - 1)
        end = str(exon_list[len(exon_list) - 1][1])
        score = '0'
        # score = transcript_dict[transcript_id][1]
        strand = transcript_dict[transcript_id][2]
        RGB = '0,0,0'
        exon_num = str(len(exon_list))
        exon_sizes = ''
        exon_starts = ''
        for exon in exon_list:
            exon_size = exon[1] - exon[0] + 1
            exon_sizes = exon_sizes + str(exon_size) + ","
            exon_start = exon[0] - int(start) - 1
            exon_starts = exon_starts + str(exon_start) + ","
        BED_item = [chrom, start, end, transcript_id, score, strand, start, 
                    end, RGB, exon_num, exon_sizes, exon_starts]
        line = '\t'.join(BED_item) + '\n'
        BED_File.write(line)