from graph_algos import generationBasedOnSeacrest as hh
import networkx as nx 
import matplotlib.pyplot as plt 
import copy
import random
import math

# This is an addition to the web-app motivated by research on the paper titled
# "On Generating Realizations of Graphic Sequences with Connected k-factors and Disconnected k-factors"
# by Dr. Asish Mukhopadhyay
# This file was originally written by Lucas Sarweh starting on 07/03/2024

# The purpose of this program is to provide functions that automatically generate
# graphic sequences of certain types for experimentation

# Constructs and returns the nodes and edges for 3 graphs including
# The original graph, k-factor graph, and d - k graph
def constructGraph(degSeq, n, k):
    G1 = nx.MultiGraph()
    G2 = nx.MultiGraph()
    G3 = nx.MultiGraph()
    G4 = nx.MultiGraph()

    #create node list
    nodeList=[]
    for i in range(0,n):
        nodeList.append(i)
    DS1=[]
    DS2=[]
    edgeSum1 = 0
    edgeSum2 = 0
    # DS is a 2D that helps maintain the degree-vertex label association
    for i in range(0, n):
        #create 2 lists(One for A and another for B)
        DS1.append([nodeList[i],degSeq[i]])
        DS2.append([nodeList[i],degSeq[i]])
        #Assign degree values for A and B
    for i in range(0,n):
        DS1[i][1] = DS1[i][1] - k
        DS2[i][1] = n - 1 - DS2[i][1]
    
    print(DS1)
    print(DS2)

    DS1=sorted(DS1,key=lambda x:x[1], reverse=False)
    DS2=sorted(DS2,key=lambda x:x[1], reverse=False)
    
    for i in range(n-1):
        edgeSum1 = edgeSum1 + DS1[i][1]
        edgeSum2 = edgeSum2 + DS2[i][1]
    
    if (edgeSum1 + DS1[n-1][1])%2 != 0 or edgeSum1 < DS1[n-1][1] or (edgeSum2 + DS2[n-1][1])%2 != 0 or edgeSum2 < DS2[n-1][1]:
        print('graph is not realizable')
        quit()
    M1 = []
    M2 = []
    M3 = []
    M4 = []
    #Create Graph A
    hh.constructGraph(n, DS1, G1)
    print(G1.has_edge(0,2))
    hh.removeMultipleEdges(G1) #remove multiple edges
    #hh.displayGraph(G1, 'Graph A')
    #hh.displayGraph(G1)
    hh.createAdjacencyMatrix(G1, M1, n)
    #Create Graph B
    hh.constructGraph(n, DS2, G2)
    hh.removeMultipleEdges(G2)
    hh.createAdjacencyMatrix(G2, M2, n)

    #SuperImpose Graph A and B to get common edges
    M = hh.superImposeGraph(M1, M2, n)
    #remove common edges by edge switching
    hh.removeSuperimposingEdges(G1, G2, M, n)
    
    #hh.displayGraph(G2, 'Graph B')
    
    hh.createAdjacencyMatrix(G2, M3, n)

    #compute B complement
    hh.complementGraph(M3, n)
    hh.createGraphFromMatrix(G3, M3, n)
    print(G3.edges)
    #hh.displayGraph(G3, 'Graph B complement')

    hh.createAdjacencyMatrix(G1, M4, n)

    #Subtract A from B complement
    Mf = hh.subtractGraph(M3, M4, n)
    hh.createGraphFromMatrix(G4, Mf, n)
    #hh.displayGraph(G4, 'Graph (B complement)\\A')

    # Return the original graph, k-factor graph, and d-k graph
    return [{'nodeList': list(G3.nodes()), 'edgeList': list(G3.edges())},
            {'nodeList': list(G4.nodes()), 'edgeList': list(G4.edges())},
            {'nodeList': list(G1.nodes()), 'edgeList': list(G1.edges())}]