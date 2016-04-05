# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 09:29:00 2016

@author: biochen
"""
import sys, getopt

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

#define rankdata funciton to calculate rank
def rank_simple(vector):
    return sorted(range(len(vector)), key=vector.__getitem__)

def rankdata(vector):
    n = len(vector)
    ivec = rank_simple(vector)
    svec = [vector[rank] for rank in ivec]
    sumranks = 0
    dupcount = 0
    newvector = [0] * n
    for i in range(n):
        sumranks = sumranks + i
        dupcount = dupcount + 1
        if i == n - 1 or svec[i] != svec[i + 1]:
            averank = sumranks / float(dupcount) + 1
            for j in range(i - dupcount + 1, i + 1):
                newvector[ivec[j]] = averank
            sumranks = 0
            dupcount = 0
    return newvector

#calculate rank
for node in network:
    network[node] = dict(zip(network[node][0] ,rankdata(network[node][1])))

#calculate mutual rank and output
for edge in edges:    
    rank1 = network[edge[0]][edge[1]]
    rank2 = network[edge[1]][edge[0]]
    mutual_rank = (rank1 * rank2) ** 0.5
    item = [edge[0], edge[1], mutual_rank]
    line = edge[0] + "\t" + edge[1] + "\t" + str(mutual_rank) + "\n"
    netwrok_out_file.write(line)   

network_in_file.close()
netwrok_out_file.close()