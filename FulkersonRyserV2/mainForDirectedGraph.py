# This algorithm proves sufficieny of fulkerson ryser theorem
# (\Sigma_{i=1}^r {od_i} \leq \Sigma_{i=1}^r min\{r-1,id_i\} + \Sigma_{i=r+1}^n min\{r,id_i\}, \forall r~such~that~1 \leq r < n)
# There are 4 cases to be handled similar to Tripathi's sufficiency proof for EGI.

from numpy import sort
import DirectedGraphGeneration as kw
import networkx as nx 
import matplotlib.pyplot as plt
import random

class HHTree:
    def __init__(self,n,degSeq, G):
        self.n=n
        self.degSeq = degSeq
        self.G=nx.MultiDiGraph()

if __name__ == '__main__':          
    minDeg = int(input("Enter the minimum Degree:"))
    maxDeg = int(input("Enter the maximum Degree:"))
    if minDeg > maxDeg:
        print('min degree cannot be greater than max degree')
        exit()
    n = max(2*(maxDeg-minDeg), ((maxDeg + minDeg +1)**2)/(4*minDeg))
    n = int(n)
    degList=[]
    degList = kw.GenerateDegrees(n, minDeg, maxDeg)
    print ("Undirected degree sequence", degList)
    
    degSum = sum(degList)
    outDegSum = 0
    outDegList = []
    inDegList = []

    #Out degree generation
    for i in range(n):
        #generate at random with the undireected degree at that index as the upper bound
        outDeg = random.randint(1, degList[i])
        #check if the random number makes the out-degree sum exceed (total degree sum /2)
        if (outDegSum + outDeg > degSum/2):
            # if it exceeds then assign ou-degree such that the out-degree results in out-degree sum = (total degree sum /2)
            outDeg = degSum/2 - outDegSum
        outDegList.append(int(outDeg))
        outDegSum = outDegSum + outDeg
    
    # if out degree sum is not equal to (total degree sum /2) then increment degree of each vertex by 1 so that the condition is met
    if (outDegSum < degSum/2):
        i = 0
        while 1:
            # first check if the out-degree is in bounds even after incrementing
            if outDegSum < degSum/2 and outDeg[i] < degList[i]:
                outDeg[i] = outDeg[i] + 1
                outDegSum = outDegSum + 1
            if outDegSum == degSum/2:
                break
            i = i+1
            if i == n:
                i = 0
    # generate in-degree which is equal to degree at the index minus the out-degree at that index
    for i in range(n):
        inDegList.append(int(degList[i] - outDegList[i]))
    
    G = nx.MultiDiGraph()
    degList1=[]
    indeg = 0
    outdeg = 0
    valid = 1

    for i in range(n):
        indeg = indeg + inDegList[i]
        outdeg = outdeg + outDegList[i]
        if (inDegList[i] >= n or outDegList[i] >= n):
            print ("graph cannot be created")
            valid = 0
        degValue = [str(outDegList[i]) + "," + str(inDegList[i]), i+1]
        print(degValue)
        degList1.append(degValue)


    # n = int(input("Enter no. of nodes, return and then enter the degrees (outdegree,indegree), one per line:")) #OK, in Python 3

    # for i in range(0, n): 
    #     degValue = [input(), i+1]
    #     v1 = int(degValue[0].split(',')[0])
    #     v2 = int(degValue[0].split(',')[1])
    #     v1 = v1 + indeg
    #     v2 = v2 + outdeg
    #     if (v1 >= n or v2 >= n):
    #         print ("graph cannot be created")
    #         valid = 0
    #     degList1.append(degValue) # adding the element
    if (indeg != outdeg):
        valid = 0
    if (valid == 1):
        sortedDegList = kw.sortVertices(degList1, n)
        kw.constructDirectedGraph(G, sortedDegList, n)
        kw.displayGraph(G)

