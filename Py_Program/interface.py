import sys
import chordalGraphUnified_V4 as CG

# number of nodes and edges
if not len(sys.argv) == 3:
    exit()

noNodes = int(sys.argv[1])
noEdges = int(sys.argv[2])

# onCreateCoGClick
initGraph = CG.ChordalGraph(noNodes, noEdges)

initGraph.createCT(initGraph.completeGraph)

initGraph.createCGByDeletion()
initGraph.dfsCaller()
initGraph.rip()

initGraph.dictToJSON(initGraph.chordalGraph)
print(initGraph.graphInJSON)
# initGraph.printInfo(initGraph.chordalGraph)