# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 22:57:17 2016

@author: biochen
"""

import sys, getopt
from scipy.stats import rankdata

opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
for op, value in opts:
    if op == "-i":
        network_in_file_name = value
    elif op == "-o":
        netwrok_out_file_name = value
    elif op == "-h":
        print("Usage: python mutual_rank.py -i raw.network -o mutual_rank.network")
        sys.exit()

network_in_file = open(network_in_file_name, "r")
netwrok_out_file = open(netwrok_out_file_name, "w")

#Load the network to generate a dict
network = {}
edges = []
for line in network_in_file:
    line = line.rstrip()
    item = line.split()
    edges.append([item[0], item[1]])
    if item[0] in network:
        network[item[0]][0].append(item[1])
        network[item[0]][1].append(-float(item[2]))
    else:
        network[item[0]] = [[], []]
        network[item[0]][0].append(item[1])
        network[item[0]][1].append(-float(item[2]))
    if item[1] in network:
        network[item[1]][0].append(item[0])
        network[item[1]][1].append(-float(item[2]))
    else:
        network[item[1]] = [[], []]
        network[item[1]][0].append(item[0])
        network[item[1]][1].append(-float(item[2]))

#calculate rank
for node in network:
    network[node] = dict(zip(network[node][0] ,list(rankdata(network[node][1]))))

#calculate mutual rank and output
for edge in edges:    
    rank1 = network[edge[0]][edge[1]]
    rank2 = network[edge[1]][edge[0]]
    mutual_rank = (rank1 * rank2) ** 0.5
    line = edge[0] + "\t" + edge[1] + "\t" + str(mutual_rank) + "\n"
    netwrok_out_file.write(line)

network_in_file.close()
netwrok_out_file.close()