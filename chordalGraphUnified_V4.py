import random
import copy
import numpy as np
import networkx as nx # used this only for converting "dictionary typed graph to networkx graph" for visualization with matplotlib
#import matplotlib.pyplot as plt #python plotting library
import itertools
import collections
import json
from functools import reduce

class ChordalGraph:
    """This class turns the chordal gaph into weakly chordal graph. During this process it generates our cycle for the given 
    number of vertices and and the number of edges."""
    def __init__(self, noNodes, noEdges):
        self.noNodes = noNodes
        self.noEdges = noEdges
        self.treeEdges = 0
        self.edgeList = []
        self.completeGraph = {}
        self.verticesList = []
        self.chordalTree = {}
        self.prev_card = 0
        self.L = [[] for _ in range(noNodes+2)]
        self.s = 0
        self.cliqueTree = {}
        self.cliqueTreeNames = {}
        self.cliqueTreeRIP = []
        self.visited = []
        self.alpha = []
        self.revAlpha = []
        self.chordalGraph = {}
        #self.edgePairs = []
        
    def createCompleteGraph(self):
        """function to create general tree"""
        pass
        #self.verticesList = [v for v in range(self.noNodes)]
        #for v in self.verticesList:
            #adjV = []
            #adjV = copy.deepcopy(self.verticesList)
            #adjV.remove(v)
            #self.completeGraph.update({v:adjV})
        #completeGraphNX = nx.complete_graph(self.noNodes)
        #self.completeGraph = nx.to_dict_of_lists(completeGraphNX)
        
        #self.completeGraph = {0: [1, 2, 3],
                              #1: [0, 2, 3],
                              #2: [0, 1, 3],
                              #3: [0, 1, 2]}
        #self.completeGraph = {0: [1, 2, 3, 4],
                              #1: [0, 3, 4],
                              #2: [0, 3, 4],
                              #3: [0, 1, 2, 4],
                              #4: [0, 1, 2, 3]}
        #self.completeGraph = {0: [1, 2, 3, 4],
                              #1: [0, 3, 4],
                              #2: [0, 4],
                              #3: [0, 1],
                              #4: [0, 1, 2]}
        #self.completeGraph = {0: [1, 2, 4, 5],
                              #1: [0, 2],
                              #2: [0, 1, 3, 4],
                              #3: [2, 4],
                              #4: [0, 2, 3, 5],
                              #5: [0, 4]}
        #self.completeGraph = {0: [1, 2, 3, 4, 5],
                              #1: [0, 2],
                              #2: [0, 1, 3],
                              #3: [0, 2, 4],
                              #4: [0, 3, 5],
                              #5: [0, 4]}   
        #self.completeGraph = {0: [1, 2, 3, 4, 5],
                              #1: [0, 2],
                              #2: [0, 1, 3],
                              #3: [0, 2, 4],
                              #4: [0, 3, 5],
                              #5: [0, 4]}
        #self.completeGraph = {0: [1, 3, 4],
                              #1: [0, 4],
                              #2: [4],
                              #3: [0, 4],
                              #4: [0, 1, 2, 3]}
        #self.completeGraph = {0: [2, 4],
                              #1: [2, 3],
                              #2: [0, 1, 3, 4],
                              #3: [1, 2],
                              #4: [0, 2]}
        #self.completeGraph = {0: [1, 2, 3, 4],
                              #1: [0, 2, 3, 4],
                              #2: [0, 1, 3, 4],
                              #3: [0, 1, 2, 4],
                              #4: [0, 1, 2, 3]}
        #self.inputCompleteGraph = copy.deepcopy(self.completeGraph)
 
    def createTree(self): 
        """function to create general tree"""        
        self.treeEdges = self.noNodes-1 #treeEdges = self.chordalTree-1
        
        for i in range(0, self.noNodes): 
            if not self.chordalTree:
                self.chordalTree[i] = list()
            elif i == 1:
                self.chordalTree[i-1].append(i)
                self.chordalTree[i] = list()
                self.chordalTree[i].append(i-1)
            else:
                methods = random.randint(1, 2)
                currentNodes = list(self.chordalTree.keys())
                if methods == 1:    # add a new node
                    v1 = random.choice(currentNodes)
                    self.addANode(v1, i) # i is the new node
                elif methods == 2:  # split an existing edge
                    while True:
                        v1 = random.choice(currentNodes)
                        if self.chordalTree[v1]:
                            v2 = random.choice(self.chordalTree[v1])
                            break               
                    self.splitAnEdge(v1, v2, i) # i is the new node

        #################################
        #self.chordalTree = {0: [1, 2, 3],
                            #1: [0, 3],
                            #2: [0, 3],
                            #3: [0, 1, 2]}
        #self.chordalTree = {0: [1],
                            #1: [0, 2, 3],
                            #2: [1],
                            #3: [1]}
        #self.chordalTree = {0: [1, 2, 3, 4], 
                            #1: [0], 
                            #2: [0], 
                            #3: [0], 
                            #4: [0, 5], 
                            #5: [4]}
        #self.chordalTree = {0: [5], 
                            #1: [2], 
                            #2: [1, 3, 4, 5], 
                            #3: [2], 
                            #4: [2], 
                            #5: [0, 2]}
        #self.chordalTree = {0: [2, 6],
                            #1: [2],
                            #2: [0, 1, 7],
                            #3: [9],
                            #4: [5],
                            #5: [4, 7, 8],
                            #6: [0, 9],
                            #7: [2, 5],
                            #8: [5],
                            #9: [3, 6]}
        #################################
        
        #self.inputChordalTree = copy.deepcopy(self.chordalTree)
        
    def createEdgeList(self, graph):
        if self.chordalTree:
            for v1, v in list(graph.items()):
                for v2 in v:
                    e = []
                    if v1<v2:
                        e.append(v1)
                        e.append(v2)
                        self.edgeList.append(e)

    def createCT(self, graphToCT):
        self.cliqueTree = {}
        self.cliqueTreeNames = {}        
        if graphToCT:
            self.createEdgeList(graphToCT) ###created edgelist for (chordal) tree
            V = []
            for key,value in list(graphToCT.items()):
                V.append(key)
            
            self.s = 0    
            #for i in range(len(V), 0, -1):
            for i in reversed(V):
                v, new_card, Ks = self.chooseAVertex(i, V, graphToCT)
                self.alpha.append(v[0])
                if new_card <= self.prev_card:
                    self.s = self.s+1
                    #self.cliqueTreeNames[self.s] = list()
                    #for ks in Ks:
                        #self.cliqueTreeNames[self.s].append(ks)
                    if new_card != 0:
                        k = self.findMin(Ks)
                        for key, value in list(self.cliqueTreeNames.items()):
                            if k in value:
                                p = key
                        #p = self.cliqueTreeNames.keys()[self.cliqueTreeNames.values().index(k)]
                        if self.s in self.cliqueTree:
                            self.cliqueTree[self.s].append(p)
                        else:
                            self.cliqueTree[self.s] = list()
                            self.cliqueTree[self.s].append(p)
                            self.cliqueTreeRIP.append(self.s) ###
                        if p in self.cliqueTree:
                            self.cliqueTree[p].append(self.s)
                        else:
                            self.cliqueTree[p] = list()
                            self.cliqueTree[p].append(self.s)
                            self.cliqueTreeRIP.append(p) ###
                    self.cliqueTreeNames[self.s] = list()
                    for ks in Ks:
                        self.cliqueTreeNames[self.s].append(ks)
                if self.s not in self.cliqueTree:
                    self.cliqueTree[self.s] = list()
                    self.cliqueTreeRIP.append(self.s)
                if self.s in self.cliqueTreeNames:
                    self.cliqueTreeNames[self.s].append(v[0])
                else:
                    self.cliqueTreeNames[self.s] = list()
                    self.cliqueTreeNames[self.s].append(v[0])
                self.L[i] = list(set(self.L[i+1]).union(set(v)))
                self.prev_card = new_card
            
                #for item in self.alpha[::-1]:
                    #self.revAlpha.append(item)
                #print "PEO: "+str(self.revAlpha)
                #self.generateEdgePairs()
            #print "Edge Pairs: "+str(self.edgePairs)
            #print "Clique Tree: "+str(self.cliqueTree)
            #print "Maximal Cliques: "+str(self.cliqueTreeNames)
            #print "Clique Tree (RIP): "+str(self.cliqueTreeRIP)            
        else:
            self.verticesList = [v for v in range(self.noNodes)]
            for pair in itertools.combinations(self.verticesList, 2): ###created edgelist for complete graph
                e = []
                e.append(pair[0])
                e.append(pair[1])
                self.edgeList.append(e)
            self.cliqueTree.update({1: list()})
            self.cliqueTreeNames.update({1: self.verticesList})
    
    #def generateEdgePairs(self):
        #for i in range(len(self.alpha)-1):
            #for j in range(i+1, len(self.alpha)):
                #if self.alpha[j] not in self.chordalTree[self.alpha[i]]:
                    #ij = []
                    #ij.append(self.alpha[i])
                    #ij.append(self.alpha[j])
                    #self.edgePairs.append(ij)
    
    def chooseAVertex(self, i, V, graphToCT):
        VMinusLiPlus1 = list(set(V)-set(self.L[i+1]))
        vSize = 0
        chosenV = []
        for v in VMinusLiPlus1:
            vIntLTemp = set(graphToCT[v]).intersection(set(self.L[i+1]))
            vSizeTemp = len(list(vIntLTemp))
            if vSizeTemp > vSize:
                vSize = vSizeTemp
                vIntL = vIntLTemp
                if not chosenV:
                    chosenV.append(v)
                else:
                    chosenV[0] = v
        if not chosenV:
            chosenV.append(i)
            vIntL = set(graphToCT[i-1]).intersection(set(self.L[i+1]))
            vSize = len(list(vIntLTemp))            
        return chosenV, vSize, vIntL

    def findMin(self, Ks):
        labelsDict = {}
        tempLabelsList = []
        for k in Ks:
            labelsDict.update({k:self.L[k]})
            tempLabelsList.append(self.L[k])
        minV = sorted(tempLabelsList, key=lambda l: (len(l), l))
        return list(labelsDict.keys())[list(labelsDict.values()).index(minV[0])]
        #labelsDict2 = sorted(labelsDict.items(),key=operator.itemgetter(1))
        #return labelsDict2[0][0]
       
    def createCGByDeletion(self):
        completeEdges = (self.noNodes*(self.noNodes-1))/2
        numberOfEdgesToBeDeleted = completeEdges - self.noEdges
        edgeCount = 1
        while numberOfEdgesToBeDeleted > 0:
            found = []
            u = []
            v = []
            uv = random.choice(self.edgeList)
            
            #if numberOfEdgesToBeDeleted == 10:
                #uv = [1, 3] #[4, 5]
            #elif numberOfEdgesToBeDeleted == 9:
                #uv = [0, 3] #[2, 5] 
            #elif numberOfEdgesToBeDeleted == 8:
                #uv = [1, 4] #[1, 4]
            #elif numberOfEdgesToBeDeleted == 7:
                #uv = [0, 4] #[3, 5]
            #elif numberOfEdgesToBeDeleted == 6:
                #uv = [3, 4] #[4, 6]
            #elif numberOfEdgesToBeDeleted == 5:
                #uv = [0, 1] #[0, 4]
            #elif numberOfEdgesToBeDeleted == 4:
                #uv = [2, 3] #[5, 6]
                
            #if numberOfEdgesToBeDeleted == 20:
                #uv = [1, 9]
            #elif numberOfEdgesToBeDeleted == 19:
                #uv = [1, 4]
            #elif numberOfEdgesToBeDeleted == 18:
                #uv = [4, 7]
            #elif numberOfEdgesToBeDeleted == 17:
                #uv = [1, 7]
            #elif numberOfEdgesToBeDeleted == 16:
                #uv = [4, 6]
            #elif numberOfEdgesToBeDeleted == 15:
                #uv = [5, 7]
            #elif numberOfEdgesToBeDeleted == 14:
                #uv = [1, 2]
            #elif numberOfEdgesToBeDeleted == 13:
                #uv = [7, 9]
            #elif numberOfEdgesToBeDeleted == 12:
                #uv = [6, 9]
            #elif numberOfEdgesToBeDeleted == 11:
                #uv = [2, 4]
            #elif numberOfEdgesToBeDeleted == 10:
                #uv = [6, 7]
            #elif numberOfEdgesToBeDeleted == 9:
                #uv = [1, 3]
            #elif numberOfEdgesToBeDeleted == 8:
                #uv = [3, 6]
            #elif numberOfEdgesToBeDeleted == 7:
                #uv = [2, 7]
            #elif numberOfEdgesToBeDeleted == 6:
                #uv = [0, 7]
            #elif numberOfEdgesToBeDeleted == 5:
                #uv = [1, 6]
            #elif numberOfEdgesToBeDeleted == 4:
                #uv = [4, 9]
            #elif numberOfEdgesToBeDeleted == 3:
                #uv = [6, 8]
            #elif numberOfEdgesToBeDeleted == 2:
                #uv = [2, 8]
            #elif numberOfEdgesToBeDeleted == 1:
                #uv = [5, 6]
                
            #uv = [1,4]
            #if numberOfEdgesToBeDeleted == 10:
                #uv = [2, 6] #[4, 5]
            #elif numberOfEdgesToBeDeleted == 9:
                #uv = [3, 6] #[2, 5] 
            #elif numberOfEdgesToBeDeleted == 8:
                #uv = [5, 6] #[1, 4]
            #elif numberOfEdgesToBeDeleted == 7:
                #uv = [4, 6] #[3, 5]
            #elif numberOfEdgesToBeDeleted == 6:
                #uv = [2, 3] #[4, 6]
            #elif numberOfEdgesToBeDeleted == 5:
                #uv = [1, 6] #[0, 4]
            #elif numberOfEdgesToBeDeleted == 4:
                #uv = [1, 2] #[5, 6]
            #elif numberOfEdgesToBeDeleted == 3:
                #uv = [1, 5] #[0, 2]
            #elif numberOfEdgesToBeDeleted == 2:
                #uv = [0, 2] #[0, 3]
            #elif numberOfEdgesToBeDeleted == 1:
                #uv = [0, 5] #[0, 6]
                
            u.append(uv[0])
            v.append(uv[1])

            for x, Nx in list(self.cliqueTree.items()):
                Kx = self.cliqueTreeNames[x]
                if len(list(set(uv).intersection(set(Kx))))==2:
                    found.append(x)
            if len(found) > 1 or len(self.cliqueTreeNames[found[0]]) <= 2:
                continue
            else:
                print((str(edgeCount)+ ": The edge is deleting: "+str(uv)))
                x = found[0]
                Kx = self.cliqueTreeNames[x]
                k = len(Kx)
                Nx = self.cliqueTree[x]
                
                #self.completeGraph.update({u[0]:list(set(self.completeGraph[u[0]])-set(v))})
                #self.completeGraph.update({v[0]:list(set(self.completeGraph[v[0]])-set(u))})
                
                #kxComplete = self.complete_graph_from_list(Kx)
                #kxComplete.update({u[0]:list(set(kxComplete[u[0]])-set(v))})
                #kxComplete.update({v[0]:list(set(kxComplete[v[0]])-set(u))})
                
                kxTemp = []
                kxTemp = copy.deepcopy(Kx)
                kxTemp.remove(u[0])
                kxTemp.remove(v[0])
                kxu = list(u+kxTemp)
                kxv = list(v+kxTemp)
            
                if len(self.cliqueTree) == 1:
                    #kxu = list(u+self.completeGraph[u[0]])
                    #kxv = list(v+self.completeGraph[v[0]])
                                        
                    tmpX1Node = []
                    tmpX2Node = []
                    x1 = max(self.cliqueTree, key=int)+1
                    x2 = x1+1
                    tmpX1Node.append(x1)
                    tmpX2Node.append(x2)
                    self.cliqueTree.update({x1:tmpX2Node})
                    self.cliqueTree.update({x2:tmpX1Node})
                    self.cliqueTreeNames.update({x1:kxu})
                    self.cliqueTreeNames.update({x2:kxv})
                    #self.cliqueTreeRIP.insert(self.cliqueTreeRIP.index(x)+1, x1)
                    #self.cliqueTreeRIP.insert(self.cliqueTreeRIP.index(x)+2, x2)
                    #self.cliqueTreeRIP.remove(x)
                    self.cliqueTree.pop(x, None)
                    self.cliqueTreeNames.pop(x, None)
                else:
                    #kxu = list(u+kxComplete[u[0]])
                    #kxv = list(v+kxComplete[v[0]])
                    
                    Nu = []
                    wxyu = wxyuTemp = 0
                    for y in Nx:
                        Ky = self.cliqueTreeNames[y]
                        if u[0] in Ky:
                            Nu.append(y)
                            #wxyuTemp = len(list(set(kxu).intersection(set(Ky)))) ###
                            #if wxyuTemp == k-1:
                                #wxyu = wxyuTemp
                            
                    Nv = []
                    wxyv = wxyvTemp = 0
                    for z in Nx:
                        Kz = self.cliqueTreeNames[z]
                        if v[0] in Kz:
                            Nv.append(z)
                            #wxyvTemp = len(list(set(kxv).intersection(set(Kz)))) ###
                            #if wxyvTemp == k-1:
                                #wxyv = wxyvTemp
                            
                    NuvNot = []
                    for w in Nx:
                        Kw = self.cliqueTreeNames[w]
                        if u[0] not in Kw and v[0] not in Kw:
                            NuvNot.append(w)
                                    
                    tmpX1Node = []
                    tmpX2Node = []
                    x1 = max(self.cliqueTree, key=int)+1
                    x2 = x1+1
                    tmpX1Node.append(x1)
                    tmpX2Node.append(x2)
                    self.cliqueTree.update({x1:tmpX2Node})
                    self.cliqueTree.update({x2:tmpX1Node})
                    self.cliqueTreeNames.update({x1:kxu})
                    self.cliqueTreeNames.update({x2:kxv})
                    #self.cliqueTreeRIP.insert(self.cliqueTreeRIP.index(x)+1, x1)
                    #self.cliqueTreeRIP.insert(self.cliqueTreeRIP.index(x)+2, x2)
                    
                    for y in Nu:
                    #for y in Nx:
                        #if y in Nu:
                        yList = []
                        yList.append(y)
                        self.cliqueTree.update({x1:list(set(yList+self.cliqueTree[x1]))})
                        #if x in self.cliqueTreeRIP:
                            #self.cliqueTreeRIP.insert(self.cliqueTreeRIP.index(x), self.cliqueTreeRIP.pop(self.cliqueTreeRIP.index(x1)))
                            #self.cliqueTreeRIP.remove(x)
                        self.cliqueTree.pop(x, None)
                        self.cliqueTreeNames.pop(x, None)
                        yNeighbors = []
                        yNeighbors = self.cliqueTree[y]
                        if x in yNeighbors:
                            yNeighbors.remove(x)
                            yNeighbors.append(x1)
                            self.cliqueTree.update({y:yNeighbors})
                    #else:
                        #if x in self.cliqueTree[y]:
                            #self.cliqueTree[y].remove(x)
                    
                    for z in Nv:       
                    #for z in Nx:
                        #if z in Nv:
                        zList = []
                        zList.append(z)                            
                        self.cliqueTree.update({x2:list(set(zList+self.cliqueTree[x2]))})
                        #if x in self.cliqueTreeRIP:
                            #self.cliqueTreeRIP.insert(self.cliqueTreeRIP.index(x), self.cliqueTreeRIP.pop(self.cliqueTreeRIP.index(x2)))
                            #self.cliqueTreeRIP.remove(x)
                        self.cliqueTree.pop(x, None)
                        self.cliqueTreeNames.pop(x, None)
                        zNeighbors = []
                        zNeighbors = self.cliqueTree[z]
                        if x in zNeighbors:
                            zNeighbors.remove(x)
                            zNeighbors.append(x2)
                            self.cliqueTree.update({z:zNeighbors})
                    #else:
                        #if x in self.cliqueTree[z]:
                            #self.cliqueTree[z].remove(x)
                                
                    for w in NuvNot:
                        #if w in NuvNot:
                        wList = []
                        wList.append(w)
                        tmpXNodes = []
                        tmpXNodes.append(x1)
                        tmpXNodes.append(x2)
                        arbitraryX = random.sample(tmpXNodes, 1)
                        #arbitraryX = []
                        #arbitraryX.append(3) ###
                        self.cliqueTree.update({arbitraryX[0]:list(set(wList+self.cliqueTree[arbitraryX[0]]))})
                        #if x in self.cliqueTreeRIP:
                            #self.cliqueTreeRIP.insert(self.cliqueTreeRIP.index(x), self.cliqueTreeRIP.pop(self.cliqueTreeRIP.index(arbitraryX[0])))
                            #self.cliqueTreeRIP.remove(x)
                        self.cliqueTree.pop(x, None)
                        self.cliqueTreeNames.pop(x, None)
                        wNeighbors = []
                        wNeighbors = self.cliqueTree[w]
                        if x in wNeighbors:
                            wNeighbors.remove(x)
                            wNeighbors.append(arbitraryX[0])
                        self.cliqueTree.update({w:wNeighbors})
                        #self.cliqueTree.update({w:list(set(self.cliqueTree[w]+arbitraryX))})
                    
                    for yi in Nu:
                        Kyi = self.cliqueTreeNames[yi]
                        wxyu = len(list(set(kxu).intersection(set(Kyi))))
                        
                        if wxyu == k-1:
                            #arbitraryYi = random.sample(Nu, 1)
                            arbitraryYi = []
                            arbitraryYi.append(yi)
                            
                            if x1 in self.cliqueTree:
                                self.cliqueTree.update({x1:list(set(self.cliqueTree[x1])-set(arbitraryYi))})
                                self.cliqueTree.update({arbitraryYi[0]:list(set(self.cliqueTree[arbitraryYi[0]])-set(tmpX1Node))})
                                
                                x1Neighbors = self.cliqueTree[x1]
                                for x1N in x1Neighbors:
                                    self.cliqueTree[x1N].remove(x1)
                                    self.cliqueTree[x1N].append(arbitraryYi[0])
                                
                                self.cliqueTree.update({arbitraryYi[0]:list(set(self.cliqueTree[arbitraryYi[0]]+self.cliqueTree[x1]))})
                                #print "Clique "+str(x1)+" is contracted by clique "+str(arbitraryYi[0])
                                #if x1 in self.cliqueTreeRIP:
                                    #if self.cliqueTreeRIP.index(arbitraryYi[0]) < self.cliqueTreeRIP.index(x1):
                                        #self.cliqueTreeRIP.remove(x1)
                                    #else:
                                        #self.cliqueTreeRIP.insert(self.cliqueTreeRIP.index(x1), self.cliqueTreeRIP.pop(self.cliqueTreeRIP.index(arbitraryYi[0])))
                                        #self.cliqueTreeRIP.remove(x1)
                                self.cliqueTree.pop(x1, None)
                                self.cliqueTreeNames.pop(x1, None)
                    
                    for zi in Nv:
                        Kzi = self.cliqueTreeNames[zi]
                        wxyv = len(list(set(kxv).intersection(set(Kzi))))
                        
                        if wxyv == k-1:
                            #arbitraryZi = random.sample(Nv, 1)
                            arbitraryZi = []
                            arbitraryZi.append(zi)                            
                            
                            if x2 in self.cliqueTree:
                                self.cliqueTree.update({x2:list(set(self.cliqueTree[x2])-set(arbitraryZi))})
                                self.cliqueTree.update({arbitraryZi[0]:list(set(self.cliqueTree[arbitraryZi[0]])-set(tmpX2Node))})
                                
                                x2Neighbors = self.cliqueTree[x2]
                                for x2N in x2Neighbors:
                                    self.cliqueTree[x2N].remove(x2)
                                    self.cliqueTree[x2N].append(arbitraryZi[0])
                                
                                self.cliqueTree.update({arbitraryZi[0]:list(set(self.cliqueTree[arbitraryZi[0]]+self.cliqueTree[x2]))})
                                
                                #print "Clique "+str(x2)+" is contracted by clique "+str(arbitraryZi[0])
                                #if x2 in self.cliqueTreeRIP:
                                    #if self.cliqueTreeRIP.index(arbitraryZi[0]) < self.cliqueTreeRIP.index(x2):
                                        #self.cliqueTreeRIP.remove(x2)
                                    #else:                            
                                        #self.cliqueTreeRIP.insert(self.cliqueTreeRIP.index(x2), self.cliqueTreeRIP.pop(self.cliqueTreeRIP.index(arbitraryZi[0])))
                                        #self.cliqueTreeRIP.remove(x2)
                                self.cliqueTree.pop(x2, None)
                                self.cliqueTreeNames.pop(x2, None)
                
                #if uv == [0, 5]:
                    #print uv
                self.edgeList.remove(uv)
                numberOfEdgesToBeDeleted = numberOfEdgesToBeDeleted - 1
                edgeCount = edgeCount + 1
                
        #print "Clique Tree (RIP): "+str(self.cliqueTreeRIP)
    
    def dfs(self, node):
        if node not in self.visited:
            self.visited.append(node)
            for n in self.cliqueTree[node]:
                self.dfs(n)
                
    def dfsCaller(self):
        #self.cliqueTree = {0: [2],
                            #1: [2],
                            #2: [0, 1, 3],
                            #3: [2]}
        #self.cliqueTreeNames = {0: [1, 3],
                            #1: [0, 1],
                            #2: [1, 4],
                            #3: [3, 4]}
        self.visited = []
        if len(self.cliqueTree) == 1:
            self.dfs(random.choice(list(self.cliqueTree)))
        else:
            for node, neighbors in list(self.cliqueTree.items()):
                if len(neighbors) == 1 and node not in self.visited:
                    self.dfs(node)
    
    def rip(self):
        self.chordalGraph = {}
        listOld = []
        
        for cTNL in self.visited:
        #for cTNL in self.cliqueTreeRIP:
        #for cTNL in reversed(self.cliqueTreeRIP):
            clique = self.cliqueTreeNames[cTNL]
            listNew = list(set(clique)-set(listOld))
            listCommon = list(set(clique).intersection(set(listOld)))
            for lN in listNew:
                listC = []
                listC.append(lN)
                if lN not in self.chordalGraph:
                    self.chordalGraph[lN] = []
                listAdj = list(set(clique)-set(listC))
                for l in listAdj:
                    self.chordalGraph[lN].append(l)
                    if lN not in listOld:
                        listOld.append(lN)
                
            for lC in listCommon:
                for lN in listNew:
                    self.chordalGraph[lC].append(lN)
        #print self.chordalGraph
    
    def bfs_shortest_path(self, start, goal):
        # keep track of explored nodes
        explored = []
        # keep track of all the paths to be checked
        queue = [[start]]
     
        # return path if start is goal
        if start == goal:
            return "Start = Goal"
     
        # keeps looping until all possible paths have been checked
        while queue:
            # pop the first path from the queue
            path = queue.pop(0)
            # get the last node from the path
            node = path[-1]
            if node not in explored:
                neighbours = self.cliqueTree[node]
                # go through all neighbour nodes, construct a new path and
                # push it into the queue
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    # return path if neighbour is goal
                    if neighbour == goal:
                        return new_path
     
                # mark node as explored
                explored.append(node)
     
        # in case there's no path between the 2 nodes
        return "A connecting path doesn't exist"
    
    def createCGByInsertion(self):
        treeEdges = self.noNodes-1
        numberOfEdgesToBeInserted = self.noEdges - treeEdges
        edgeCount = 1
        while numberOfEdgesToBeInserted > 0:
            foundXY = False
            
            ###Deterministic Implementation###
            #while not foundXY:
                #xAll = []
                #yAll = []
                #u = []
                #v = []
                ##for e in self.edgePairs:
                #u.append(self.edgePairs[0][0])
                #v.append(self.edgePairs[0][1])
                #for key, value in self.cliqueTree.iteritems():
                    #Kxy = self.cliqueTreeNames[key]
                    #if u[0] in Kxy:
                        #xAll.append(key)
                        ##break
                    #elif v[0] in Kxy:
                        #yAll.append(key)
                        ##break
                
                ###########
                ##print self.cliqueTreeNames
                ##CTD = nx.Graph(self.cliqueTree)
                ##pos = nx.spring_layout(CTD)
                ##plt.figure()
                ##plt.title("Clique Tree: "+str(self.cliqueTreeNames))
                ##nx.draw_networkx(CTD, pos, True)
                ##plt.show(block=False)
                ###########
                
                #if len(xAll) <= len(yAll):
                    #commonNeighbors = []
                    #zAll = copy.deepcopy(xAll)
                    #for z in zAll:
                        #neighborsOfZ = list(set(self.cliqueTree[z]).intersection(set(yAll)))
                        #commonNeighbors = commonNeighbors+neighborsOfZ
                    #if not commonNeighbors:
                        #commonNeighbors = copy.deepcopy(yAll)
                        ##for z in zAll:
                            ##for y in yAll:
                                ##neighborsOfZ = len(list(set(self.cliqueTreeNames[z]).intersection(set(self.cliqueTreeNames[y]))))
                                ##if neighborsOfZ >= 1:
                                    ##temp = []
                                    ##temp.append(y)
                                    ##commonNeighbors = commonNeighbors+temp
                        ##if commonNeighbors < yAll:
                            ##print "YesY"
                            
                    #for xi in xAll:
                        #for yj in commonNeighbors:
                            #Kxi = self.cliqueTreeNames[xi]
                            #Kyj = self.cliqueTreeNames[yj]
                            #wxy = len(list(set(Kxi).intersection(set(Kyj))))
                            #if wxy >= 1:
                                #if xi in self.cliqueTree[yj] and not foundXY:
                                    #I = list(set(Kxi).intersection(set(Kyj)))
                                    #ISize = len(I)
                                    #print str(edgeCount)+ ": The edge is adding: "+str(u+v)
                                    ##if (u+v) in self.backlogEdgePairs:
                                        ##self.backlogEdgePairs.remove(u+v)
                                    #self.edgePairs.remove(u+v)
                                    #foundXY = True
                                    #x = []
                                    #x.append(xi)
                                    #y = []
                                    #y.append(yj)
                                    #Kx = self.cliqueTreeNames[xi]
                                    #Ky = self.cliqueTreeNames[yj]
                                    #KxSize = len(Kx)
                                    #KySize = len(Ky)
                                    #break
                                #elif xi not in self.cliqueTree[yj] and not foundXY:
                                    #path = self.bfs_shortest_path(xi, yj)
                                    #w = self.noNodes
                                    #for i in range(len(path)-1):
                                        #j = i + 1
                                        #wTemp = len(list(set(self.cliqueTreeNames[path[i]]).intersection(set(self.cliqueTreeNames[path[j]]))))
                                        #if wTemp == wxy and wTemp > 0:
                                            #I = list(set(Kxi).intersection(set(Kyj)))
                                            #ISize = len(I)                        
                                            #print str(edgeCount)+ ": The edge is adding: "+str(u+v)
                                            ##if (u+v) in self.backlogEdgePairs:
                                                ##self.backlogEdgePairs.remove(u+v)
                                            #self.edgePairs.remove(u+v)
                                            #foundXY = True
                                            #x = []
                                            #x.append(xi)
                                            #y = []
                                            #y.append(yj)
                                            #Kx = self.cliqueTreeNames[xi]
                                            #Ky = self.cliqueTreeNames[yj]
                                            #KxSize = len(Kx)
                                            #KySize = len(Ky)                                        
                                            #ei = []
                                            #ej = []
                                            #ei.append(path[i])
                                            #ej.append(path[j])
                                            #self.cliqueTree.update({ei[0]:list(set(self.cliqueTree[ei[0]])-set(ej))})
                                            #self.cliqueTree.update({ej[0]:list(set(self.cliqueTree[ej[0]])-set(ei))})
                                            #self.cliqueTree.update({x[0]:self.cliqueTree[x[0]]+y})
                                            #self.cliqueTree.update({y[0]:self.cliqueTree[y[0]]+x})
                                            #break                    
                #else:
                    #commonNeighbors = []
                    #zAll = copy.deepcopy(yAll)
                    #for z in zAll:
                        #neighborsOfZ = list(set(self.cliqueTree[z]).intersection(set(xAll)))
                        #commonNeighbors = commonNeighbors+neighborsOfZ
                    #if not commonNeighbors:
                        #commonNeighbors = copy.deepcopy(xAll)
                        ##for z in zAll:
                            ##for x in xAll:
                                ##neighborsOfZ = len(list(set(self.cliqueTreeNames[z]).intersection(set(self.cliqueTreeNames[x]))))
                                ##if neighborsOfZ >= 1:
                                    ##temp = []
                                    ##temp.append(x)
                                    ##commonNeighbors = commonNeighbors+temp
                        ##if commonNeighbors < xAll:
                            ##print "YesX"
                        
                    #for xi in yAll:
                        #for yj in commonNeighbors:
                            #Kxi = self.cliqueTreeNames[xi]
                            #Kyj = self.cliqueTreeNames[yj]
                            #wxy = len(list(set(Kxi).intersection(set(Kyj))))
                            #if wxy >= 1:
                                #if xi in self.cliqueTree[yj] and not foundXY:
                                    #I = list(set(Kxi).intersection(set(Kyj)))
                                    #ISize = len(I)
                                    #print str(edgeCount)+ ": The edge is adding: "+str(u+v)
                                    ##if (u+v) in self.backlogEdgePairs:
                                        ##self.backlogEdgePairs.remove(u+v)
                                    #self.edgePairs.remove(u+v)
                                    #foundXY = True
                                    #x = []
                                    #x.append(xi)
                                    #y = []
                                    #y.append(yj)
                                    #Kx = self.cliqueTreeNames[xi]
                                    #Ky = self.cliqueTreeNames[yj]
                                    #KxSize = len(Kx)
                                    #KySize = len(Ky)
                                    #break
                                #elif xi not in self.cliqueTree[yj] and not foundXY:
                                    #path = self.bfs_shortest_path(xi, yj)
                                    #w = self.noNodes
                                    #for i in range(len(path)-1):
                                        #j = i + 1
                                        #wTemp = len(list(set(self.cliqueTreeNames[path[i]]).intersection(set(self.cliqueTreeNames[path[j]]))))
                                        #if wTemp == wxy and wTemp > 0:
                                            #I = list(set(Kxi).intersection(set(Kyj)))
                                            #ISize = len(I)                        
                                            #print str(edgeCount)+ ": The edge is adding: "+str(u+v)
                                            ##if (u+v) in self.backlogEdgePairs:
                                                ##self.backlogEdgePairs.remove(u+v)
                                            #self.edgePairs.remove(u+v)
                                            #foundXY = True
                                            #x = []
                                            #x.append(xi)
                                            #y = []
                                            #y.append(yj)
                                            #Kx = self.cliqueTreeNames[xi]
                                            #Ky = self.cliqueTreeNames[yj]
                                            #KxSize = len(Kx)
                                            #KySize = len(Ky)                                        
                                            #ei = []
                                            #ej = []
                                            #ei.append(path[i])
                                            #ej.append(path[j])
                                            #self.cliqueTree.update({ei[0]:list(set(self.cliqueTree[ei[0]])-set(ej))})
                                            #self.cliqueTree.update({ej[0]:list(set(self.cliqueTree[ej[0]])-set(ei))})
                                            #self.cliqueTree.update({x[0]:self.cliqueTree[x[0]]+y})
                                            #self.cliqueTree.update({y[0]:self.cliqueTree[y[0]]+x})
                                            #break
            ###Deterministic Implementation###
            
            ###Random Implementation###
            cliqueTreeNodes = []
            for node, neighbors in list(self.cliqueTree.items()):
                cliqueTreeNodes.append(node)
            while not foundXY:
                xy = random.sample(cliqueTreeNodes, 2)
                #if numberOfEdgesToBeInserted == 4:
                    #xy = [2, 5]
                #elif numberOfEdgesToBeInserted == 3:
                    #xy = [1, 6]
                #elif numberOfEdgesToBeInserted == 2:
                    #xy = [7, 4]
                #if numberOfEdgesToBeInserted == 9:
                    #xy = [4, 2]
                #elif numberOfEdgesToBeInserted == 8:
                    #xy = [5, 6]
                x = []
                y = []
                x.append(xy[0])
                y.append(xy[1])
                Kx = self.cliqueTreeNames[x[0]]
                Ky = self.cliqueTreeNames[y[0]]
                KxSize = len(Kx)
                KySize = len(Ky)
                wxy = len(list(set(Kx).intersection(set(Ky))))
                if wxy >= 1:
                    if x[0] in self.cliqueTree[y[0]]:
                        I = list(set(Kx).intersection(set(Ky)))
                        ISize = len(I)
                    
                        us = list(set(Kx)-set(I))
                        vs = list(set(Ky)-set(I))
                        u = random.sample(us, 1)
                        v = random.sample(vs, 1)
                        #if numberOfEdgesToBeInserted == 8:
                            #v = [5]
                        print((str(edgeCount)+ ": The edge is adding: "+str(u+v)))
                        foundXY = True
                    elif x[0] not in self.cliqueTree[y[0]]:
                        path = self.bfs_shortest_path(x[0], y[0])
                        w = self.noNodes
                        for i in range(len(path)-1):
                            j = i + 1
                            wTemp = len(list(set(self.cliqueTreeNames[path[i]]).intersection(set(self.cliqueTreeNames[path[j]]))))
                            if wTemp == wxy and wTemp > 0:
                                I = list(set(Kx).intersection(set(Ky)))
                                ISize = len(I)
                            
                                us = list(set(Kx)-set(I))
                                vs = list(set(Ky)-set(I))
                                u = random.sample(us, 1)
                                v = random.sample(vs, 1)
                                print((str(edgeCount)+ ": The edge is adding: "+str(u+v)))
                                foundXY = True
                                ei = []
                                ej = []
                                ei.append(path[i])
                                ej.append(path[j])
                                self.cliqueTree.update({ei[0]:list(set(self.cliqueTree[ei[0]])-set(ej))})
                                self.cliqueTree.update({ej[0]:list(set(self.cliqueTree[ej[0]])-set(ei))})
                                self.cliqueTree.update({x[0]:self.cliqueTree[x[0]]+y})
                                self.cliqueTree.update({y[0]:self.cliqueTree[y[0]]+x})
                                break
            ###Random Implementation###
            
            #self.chordalTree.update({u[0]:list(set(self.chordalTree[u[0]]+v))})
            #self.chordalTree.update({v[0]:list(set(self.chordalTree[v[0]]+u))})
                         
            Iuv = copy.deepcopy(I)+u+v
            #Kz = self.complete_graph_from_list(Iuv)
            zList = []
            z = max(self.cliqueTree, key=int)+1
            zList.append(z)
            
            self.cliqueTree.update({x[0]:list(set(self.cliqueTree[x[0]])-set(y))})
            self.cliqueTree.update({y[0]:list(set(self.cliqueTree[y[0]])-set(x))})
            
            self.cliqueTree.update({x[0]:self.cliqueTree[x[0]]+zList})
            self.cliqueTree.update({y[0]:self.cliqueTree[y[0]]+zList})
            self.cliqueTree.update({z:x+y})
            self.cliqueTreeNames.update({z:Iuv})
            #self.cliqueTreeRIP.append(z)
            #self.cliqueTreeRIP.append(self.cliqueTreeRIP.index(x), x1)
            #self.cliqueTreeRIP.append(self.cliqueTreeRIP.index(x), x2)
            
            if KxSize <= ISize+1:
                self.cliqueTree.update({x[0]:list(set(self.cliqueTree[x[0]])-set(zList))})
                self.cliqueTree.update({z:list(set(self.cliqueTree[z])-set(x))})
                self.cliqueTree.update({z:list(set(self.cliqueTree[z]+self.cliqueTree[x[0]]))})
                
                xNeighbors = self.cliqueTree[x[0]]
                for xN in xNeighbors:
                    self.cliqueTree[xN].remove(x[0])
                    self.cliqueTree[xN].append(z)
                    
                #print "Clique "+str(x[0])+" is contracted by clique "+str(z)
                #self.cliqueTreeRIP.remove(x[0])                
                self.cliqueTree.pop(x[0], None)
                self.cliqueTreeNames.pop(x[0], None)
                
                
            if KySize <= ISize+1:
                self.cliqueTree.update({y[0]:list(set(self.cliqueTree[y[0]])-set(zList))})
                self.cliqueTree.update({z:list(set(self.cliqueTree[z])-set(y))})                
                self.cliqueTree.update({z:list(set(self.cliqueTree[z]+self.cliqueTree[y[0]]))})
                
                yNeighbors = self.cliqueTree[y[0]]
                for yN in yNeighbors:
                    self.cliqueTree[yN].remove(y[0])
                    self.cliqueTree[yN].append(z)
                
                #print "Clique "+str(y[0])+" is contracted by clique "+str(z)
                #self.cliqueTreeRIP.remove(y[0])
                self.cliqueTree.pop(y[0], None)
                self.cliqueTreeNames.pop(y[0], None)
            
            #self.edgePairs.remove(u+v)
            self.edgeList.append(u+v)
            #self.edgePairs = self.backlogEdgePairs+self.edgePairs
            numberOfEdgesToBeInserted = numberOfEdgesToBeInserted - 1
            edgeCount = edgeCount + 1
            
        #print "Clique Tree (RIP): "+str(self.cliqueTreeRIP)
    
    def complete_graph_from_list(self, vertices):
        #vertices = [0, 1, 3]
        #edges = itertools.combinations(vertices, 2)
        #g = nx.Graph()
        #g.add_nodes_from(vertices)
        #g.add_edges_from(edges)
        #G = nx.to_dict_of_lists(g)
        #print G
        G = {}
        for v in vertices:
            adjV = []
            adjV = copy.deepcopy(vertices)
            adjV.remove(v)
            G.update({v:adjV})
        return G
    
    def addANode(self, v1, v2):
        """function to add a node in the graph"""
        self.chordalTree[v1].append(v2)
        self.chordalTree[v2] = list()
        self.chordalTree[v2].append(v1)

    def splitAnEdge(self, v1, v2, v3):
        """function to split an edge"""
        self.chordalTree[v1].remove(v2)
        self.chordalTree[v1].append(v3)

        self.chordalTree[v2].remove(v1)
        self.chordalTree[v2].append(v3)

        self.chordalTree[v3] = list()
        self.chordalTree[v3].append(v1)
        self.chordalTree[v3].append(v2)
    
    def addAnEdge(self, graph, v1, v2):
        """function to add an edge in the graph"""
        graph[v1].append(v2)
        graph[v2].append(v1)   
    
    def addMoreEdges(self, requiredMoreEdges):
        """function to add more edges in the graph: moreEdges = givenEdges - treeEdges"""
        newEdges = 0
        self.weaklyChordalGraph = copy.deepcopy(self.fourCycleDict)
        while newEdges < requiredMoreEdges:
            vertices = random.sample(self.weaklyChordalGraph, 2)
            u = vertices[0]
            v = vertices[1]
            if self.ifEdgeExist(self.weaklyChordalGraph, u, v):
                continue
            else:
                I_uv = list(set(self.weaklyChordalGraph[u]).intersection(self.weaklyChordalGraph[v]))
                if I_uv:
                    x = random.choice(I_uv)
                    auxNodes = list(set(self.weaklyChordalGraph[x]).difference(I_uv))
                    auxGraph = self.createAuxGraph(self.weaklyChordalGraph, auxNodes)
                    if not self.isReachable(auxGraph, u, v):
                        self.addAnEdge(self.weaklyChordalGraph, u, v)
                        print(("\nAdded edge between: "+str(u)+" and "+str(v)))
                        newEdges += 1
        #print self.weaklyChordalGraph
        #G = nx.Graph(self.weaklyChordalGraph)
        #if nx.is_chordal(G):
            #print "========================"
            #print "This is a Chordal graph."
            #print "========================"
            
    def ifEdgeExist(self, graph, v1, v2):
        """function to check if edge exist"""
        if v2 in graph[v1] or v1 in graph[v2]:
            return True
        else:
            return False
        
    def isReachable(self, auxGraph, v1, v2):
        """function (BFS) to check path between v1 and v2"""
        visited =[False]*(self.noNodes)
        queue=[]
        queue.append(v1)
        visited[v1] = True
  
        while queue:
            n = queue.pop(0)
            if n == v2:
                return True
            for i in auxGraph[n]:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True
        return False
                
    def createAuxGraph(self, graph, auxNodes):
        """function to creae graphs C and G[C]"""
        auxGraph = {}
        for i in auxNodes:
            if i in graph:
                auxGraph[i] = list(set(graph[i]).intersection(set(auxNodes)))
        return auxGraph
    
    def printInfo(self, graphToDraw):
        G = nx.Graph(graphToDraw)
        if nx.is_chordal(G):
            print("========================")
            print("This is a Chordal graph.")
            print("========================")
        #print "\nPrint Chordal Graph (adjacency list): "
        print(("Clique Tree: "+ str(self.cliqueTree)))
        #print "Clique Tree (RIP):"+str(self.visited)
        print(("Maximal Cliques:"+ str(self.cliqueTreeNames)))
        self.dictToJSON(graphToDraw)
        if not self.completeGraph and not self.chordalTree:
            print(("From Complete Graph (in Adjacency List): "+ str(graphToDraw)))
            print(("From Complete Graph (in JSON): "+ str(self.graphInJSON)))
        else:
            print(("From (Chordal) Tree (in Adjacency List): "+ str(graphToDraw)))
            print(("From (Chordal) Tree (in JSON): "+ str(self.graphInJSON)))
        cliqueSize = []
        for k, v in list(self.cliqueTreeNames.items()):
            cliqueSize.append(len(v))
        counter = collections.Counter(cliqueSize)
        #if self.chordalTree:
            #print "PEO: "+str(self.revAlpha)
        print(("No. of Maximal Cliques: "+ str(len(self.cliqueTreeNames))))
        print(("Min Clique Size: "+ str(min(cliqueSize))))
        print(("Max Clique Size: "+ str(max(cliqueSize))))
        print(("Mean Clique Size: "+ str(reduce(lambda x, y: x + y, cliqueSize) / len(cliqueSize))))
        print(("Sd of clique sizes: " + str(np.std(cliqueSize))))
        print(("Variance: " + str(np.var(cliqueSize))))
        print(("Maximal Cliques Frequency: " + str(counter)))
        
        #f = open('output_Chordal.txt','a')
        #print >>f, "PEO: "+str(self.revAlpha)
        #print >>f, "No. of Maximal Cliques: "+ str(len(self.cliqueTreeNames))
        #print >>f, "Min Clique Size: "+ str(min(cliqueSize))
        #print >>f, "Max Clique Size: "+ str(max(cliqueSize))
        #print >>f, "Mean Clique Size: "+ str(reduce(lambda x, y: x + y, cliqueSize) / len(cliqueSize))
        #print >>f, "Sd of clique sizes: " + str(np.std(cliqueSize))
        #print >>f, "Maximal Cliques Frequency: " + str(counter)
        #f.close()
        
    def dictToJSON(self, graphToJSON):
        self.graphInJSON = json.dumps(graphToJSON)
        
    def JSONToDict(self, graphToDict):
        self.graphInDict = json.loads(graphToDict)    
        
    def plotGraph(self, graphToDraw, graphName):
        """function plot complete graph"""
        chordalEdges = 0
        for node, degree in list(graphToDraw.items()):
            chordalEdges += len(degree)
        #if graphName == 1:
            #print "\nNo. of Complete Graph Edges: "+ str(chordalEdges/2)
        #elif graphName == 2:
            #print "\nNo. of (Chordal) Tree Edges: "+ str(chordalEdges/2)
        #elif graphName == 3:
            #print "\nNo. of Clique Tree Edges: "+ str(chordalEdges/2)
        #elif graphName == 4:
            #print "\nNo. of Chordal Graph Edges: "+ str(chordalEdges/2)
        
        GD = nx.Graph(graphToDraw) #converting "dictionary typed graph" to "networkx graph"
        pos = nx.spring_layout(GD)
    
        #plt.figure()
        #if graphName == 1:
        #    plt.title("Complete Graph")
        #elif graphName == 2:
        #    plt.title("(Chordal) Tree")
        #elif graphName == 3:
        #    plt.title("Clique Tree"+str(self.cliqueTreeNames))
        #elif graphName == 4:
        #    plt.title("Chordal Graph"+str(self.cliqueTreeNames))
        #plt.close('all')
        nx.draw_networkx(GD, pos, True)
        #limits = plt.axis('off')
        #plt.show()