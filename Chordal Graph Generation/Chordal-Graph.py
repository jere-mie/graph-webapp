import sys
import random
import copy
import itertools
import networkx as nx

# check if input supplied
if len(sys.argv) != 2:
    print("Error: must provide a integer command line argument")
    exit()

numVertices = int(sys.argv[1])

# input checking, number of vector > 2
if numVertices < 2:
    print("Error: must be greater than 2")
    exit()

# used to split the number of vectors
# into mutually independent vertices and clique (clique contains more than 2 vertices)
randSplit = random.randint(2, numVertices-1)

# random graph vertices
randomVertices = range(0, numVertices)[:randSplit]
# mutually independent vertices
miVertices = range(0, numVertices)[randSplit:]

#start with a set of vertices that AREN'T NECESSARILY A CLIQUE
#it's any graph
#n vertuces with X MI
#generate RANDOM GRAPH INSTEAD
#use connected_components
#dense_GNM_random_graph

# STEP 1
#calculate the max and minimum amount of edges for the random graph
#this is to satisfy the second argument of dense_gnm_random_graph
noEdgesMin = len(randomVertices) - 1
noEdgesMax = (len(randomVertices) * (len(randomVertices)-1) ) / 2

#generate the random graph then convert into a usable dictionary format
randomGraph = nx.dense_gnm_random_graph(len(randomVertices), random.randint(noEdgesMin, noEdgesMax+1))
connComps = sorted(nx.connected_components(randomGraph))
randomGraph = nx.to_dict_of_lists(randomGraph)

connComps = list(connComps)
numOfConnComps = len(connComps)

# Function to connect separated components of the random graph, if exist		
def addAnEdge(randomGraph, v1, v2):
	randomGraph[v1].append(v2)
	randomGraph[v2].append(v1)

if numOfConnComps > 1:
	j = 0
	while j < numOfConnComps - 1:
		u = random.choice(list(connComps[j%numOfConnComps]))
		v = random.choice(list(connComps[(j+1)%numOfConnComps]))
		addAnEdge(randomGraph, u, v)
		j = j + 1
# Print random graph
print("Random graph: " + str(randomGraph))

# STEP 2
# Convert random graph into a clique(complete graph)
# copy the randomGraph
cliqueGraph = copy.deepcopy(randomGraph)
for v in cliqueGraph:
	cliqueGraph[v] = [x for x in randomVertices if x != v]

# Print clique graph
print("Clique graph: " + str(cliqueGraph))

# STEP 3
# connect each mutually independent vertex to the clique graph
# dictionary of miVertices		

# edges contains pairs that represent edge between the clique graph
# to the mutually independent vertex
edges = []

# create edges from each mutually independent vertices to each clique vertices
# this done by taking the Cartesian product of miVertices and randomVertices
edges.extend(itertools.product(miVertices, randomVertices))

# copy the clique graph to add edge to mutually indepdent vertices
graph = copy.deepcopy(cliqueGraph)
# add mutually indepdent vertices
for v in miVertices:
	graph[v] = []
# add edge from clique graph to mutually indepdent vertices
for v1,v2 in edges:
    graph[v1].append(v2)
    graph[v2].append(v1)

# Print final graph
print("Chordal graph: " + str(graph))