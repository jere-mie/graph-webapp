import sys
import chordalGraphUnified_V4 as CG

# number of nodes and edges
if not len(sys.argv) == 5:
    exit()

noNodes = int(sys.argv[1])
noEdges = int(sys.argv[2])
btnId = sys.argv[3]

DeletionStart = False
if sys.argv[4] == 'true':
    DeletionStart = True

if btnId == "btnCompleteGraph":
    initGraph = CG.ChordalGraph(noNodes, noEdges)
    initGraph.dictToJSON(initGraph.completeGraph)
elif btnId == "btnTree":
    initGraph = CG.ChordalGraph(noNodes, noEdges)
    initGraph.createTree()
    initGraph.dictToJSON(initGraph.chordalTree)
elif btnId == "btnCliqueTree":
    initGraph = CG.ChordalGraph(noNodes, noEdges)

    if DeletionStart:
        initGraph.createCT(initGraph.completeGraph)
    else:
        initGraph.createTree()
        initGraph.createCT(initGraph.chordalTree)
    
    initGraph.dictToJSON(initGraph.cliqueTree)
elif btnId == "btnChordalGraph":
    initGraph = CG.ChordalGraph(noNodes, noEdges)

    if DeletionStart:
        initGraph.createCT(initGraph.completeGraph)
        initGraph.createCGByDeletion()
        initGraph.dfsCaller()
        initGraph.rip()
    else:
        initGraph.createTree()
        initGraph.createCT(initGraph.chordalTree)
        initGraph.createCGByInsertion()
        initGraph.dfsCaller()
        initGraph.rip()
    
    initGraph.dictToJSON(initGraph.chordalGraph)


print(initGraph.graphInJSON)

# # onCreateCoGClick
# initGraph = CG.ChordalGraph(noNodes, noEdges)

# initGraph.createCT(initGraph.completeGraph)

# initGraph.createCGByDeletion()
# initGraph.dfsCaller()
# initGraph.rip()

# initGraph.dictToJSON(initGraph.chordalGraph)
# print(initGraph.graphInJSON)
# # initGraph.printInfo(initGraph.chordalGraph)