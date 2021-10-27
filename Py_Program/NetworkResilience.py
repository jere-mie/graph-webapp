import networkx
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


# call this function to draw to screen
def drawGraph():
    # nx.spring_layout(G, k=0.15, iterations=50)
    pos = nx.spring_layout(G)
    plt.figure(3, figsize=(10, 10))
    plt.title("f = " + str(f))
    nx.draw(G, node_color=color_map, edgecolors='black', node_size=100)
    plt.show()

# function for coloring higher value nodes for better visualization
def colorHighDegreeNodes(num):
    nodes = list(G.nodes)

    for node in nodes:
        degreeTotals.append(nx.degree(G, node))

    degreeTotals.sort(reverse=True)

    highestDegreeTotals = []
    for i in range(num):
        highestDegreeTotals.append(degreeTotals[i])

    for node1 in nodes:
        if highestDegreeTotals.__contains__(len(G.edges(node1))):
            color_map.append('red')
        else:
            color_map.append('blue')

    # coloring children of highest degree nodes (not working properly)

    # for n in highestEdgeTotals:
    #     for n2 in list(nx.neighbors(G, n)):
    #         if not highestEdgeTotals.__contains__(n2):
    #             color_map[n2] = 'orange'

# ---------------different types of graphs-------------------------------------------
# scale free
G = nx.barabasi_albert_graph(130, 4, seed=None, initial_graph=None)
# G = nx.scale_free_graph(130)

# exponential
# G = nx.erdos_renyi_graph(130, 0.5)
# G = nx.gnm_random_graph(130, 215)
# ---------------------------------------------------------------------------------

f = 0.00

color_map = []

degreeTotals = []

highestEdgeTotals = []

print(highestEdgeTotals)

colorHighDegreeNodes(5) # color before removal
drawGraph() # draw graph before removal

for loop in range(19):  # change number to increase the amount of times f is increased by 5%
    edges = list(G.edges)
    nodes = list(G.nodes)

    f += 0.05

    nodesNumToBeRemoved = int(len(nodes) * f)  # calculate how many nodes to be removed

    numNodes = nx.number_of_nodes(G) # number of nodes
    G2 = G.copy() # create copy of graph so nodes can be removed safetly
    removedNodes = []
    # print(len(color_map))

    for i in range(nodesNumToBeRemoved):  # run for each time a node needs to be removed
        print("Runs: " + str(i))
        for k in range(numNodes):  # go through all nodes
            # print(str(edgeTotals[i])+" "+str(nx.degree(G2, k)))
            # check if node exist, check if node has a high value, and checks if node was not removed before
            if G2.has_node(k) and degreeTotals[i] == int(nx.degree(G2, k)) and not removedNodes.__contains__(k):
                print("Node: " + str(k) + " with " + str(nx.degree(G2, k)) + " degree was removed")
                print(color_map[list(G.nodes).index(k)])
                del color_map[list(G.nodes).index(k)]  # del color associated with node to deleted
                removedNodes.append(k) # add to list of removed nodes
                G.remove_node(k)  # remove the node
                break

    color_map = []
    degreeTotals = []

    colorHighDegreeNodes(5)
    drawGraph()

