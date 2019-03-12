import sys
import random
import itertools

# check if input supplied
if len(sys.argv) != 2:
    print("Error: must provide a integer command line argument")
    exit()

numVectors = int(sys.argv[1])

# input checking, number of vector > 2
if numVectors < 2:
    print("Error: must be greater than 2")
    exit()

# used to split the number of vectors
# into mutually independent vertices and clique (clique contains more than 2 vertices)
randSplit = random.randint(2, numVectors)

# mutually independent vertices
cVertices = range(0, numVectors)[:randSplit]
# clique vertices
miVertices = range(0, numVectors)[randSplit:]

# list of edges
edges = []

# create edges for clique
edges.extend(itertools.combinations(cVertices, 2))

# create edges from each mutually independent vertices to each clique vertices
# this done by taking the Cartesian product of miVertices and cVertices
edges.extend(itertools.product(miVertices, cVertices))

# create empty dictionary for graph
graph = {v: [] for v in range(0, numVectors)}
# convert list of edges to dictionary graph
for v1,v2 in edges:
    graph[v1].append(v2)
    graph[v2].append(v1)

print graph