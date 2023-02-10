import sys
import json
import chordalGraphUnified_V4 as CG

# arguments numNodes, numEdges, deletionStart

# number of nodes and edges
if not len(sys.argv) == 4:
    exit()
noNodes = int(sys.argv[1])
noEdges = int(sys.argv[2])

DeletionStart = False
if sys.argv[3] == 'true':
    DeletionStart = True
graphs = []

if DeletionStart:
    # create complete graph
    initGraph = CG.ChordalGraph(noNodes, noEdges)
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

# create array of graphs
output = '['
for i, graph in enumerate(graphs):
    output += str(graph)
    if i != len(graphs)-1:
        output += ', '

output += ']'
# output graphs
print(output)