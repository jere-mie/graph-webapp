import sys
import json
import graph_algos.chordalGraphUnified_V4 as CG

# arguments numNodes, numEdges, deletionStart

def generateCG(noNodes, noEdges, deletionStart):
    graphs = []
    if deletionStart:
        # create complete graph
        initGraph = CG.ChordalGraph(int(noNodes), int(noEdges))
        initGraph.dictToJSON(initGraph.completeGraph)
        graphs.append(initGraph.graphInJSON)
        # create clique tree
        initGraph.createCT(initGraph.completeGraph)
        initGraph.dictToJSON(initGraph.cliqueTree)
        graphs.append(initGraph.graphInJSON)
        # create chordal graph
        initGraph.createCGByDeletion()
        initGraph.dfsCaller()
        initGraph.rip()
        initGraph.dictToJSON(initGraph.chordalGraph)
        graphs.append(initGraph.graphInJSON)
       #initGraph.printInfo(initGraph.chordalTree)

    else:
        # create tree
        initGraph = CG.ChordalGraph(noNodes, noEdges)
        initGraph.createTree()
        initGraph.dictToJSON(initGraph.chordalTree)
        graphs.append(initGraph.graphInJSON)
        # create clique tree
        initGraph.createCT(initGraph.chordalTree)
        initGraph.dictToJSON(initGraph.cliqueTree)
        graphs.append(initGraph.graphInJSON)
        # create chordal graph
        initGraph.createCGByInsertion()
        initGraph.dfsCaller()
        initGraph.rip()
        initGraph.dictToJSON(initGraph.chordalGraph)
        graphs.append(initGraph.graphInJSON)
        #initGraph.printInfo(initGraph.chordalTree)
    return graphs