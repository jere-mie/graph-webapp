# This algorithm proves sufficieny of fulkerson ryser theorem
# (\Sigma_{i=1}^r {od_i} \leq \Sigma_{i=1}^r min\{r-1,id_i\} + \Sigma_{i=r+1}^n min\{r,id_i\}, \forall r~such~that~1 \leq r < n)
# There are 4 cases to be handled similar to Tripathi's sufficiency proof for EGI.

from numpy import sort
import DirectedGraphGeneration as kw
import networkx as nx 
import matplotlib.pyplot as plt
import copy

class HHTree:
    def __init__(self,n,degSeq, G):
        self.n=n
        self.degSeq = degSeq
        self.G=nx.MultiDiGraph()
if __name__ == '__main__':            
    n = int(input("Enter no. of nodes, return and then enter the degrees (outdegree,indegree), one per line:")) #OK, in Python 3

    G = nx.MultiDiGraph()
    degList=[]
    indeg = 0
    outdeg = 0
    valid = 1
    for i in range(0, n): 
        degValue = [input(), i+1]
        v1 = int(degValue[0].split(',')[0])
        v2 = int(degValue[0].split(',')[1])
        v1 = v1 + indeg
        v2 = v2 + outdeg
        if (v1 >= n or v2 >= n):
            print ("graph cannot be created")
            valid = 0
        degList.append(degValue) # adding the element
    if (indeg != outdeg):
        valid = 0
    if (valid == 1):
        sortedDegList = kw.sortVertices(degList, n)
        kw.constructDirectedGraph(G, sortedDegList, n)
        kw.displayGraph(G)
