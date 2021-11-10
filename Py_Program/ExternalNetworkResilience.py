import json

import networkx
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
import time
import csv


# call this function to draw to screen
def drawGraph(graph):
    print("Drawing network...")
    # nx.spring_layout(graph, k=0.5, iterations=50)
    # pos = nx.spring_layout(graph)
    plt.figure(3, figsize=(10, 10))
    plt.title("f = " + str(f))
    nx.draw(graph, node_color=color_map, edgecolors='black', node_size=30)
    plt.show()


# function for coloring higher value nodes for better visualization
def colorHighDegreeNodes(graph, num, resilienceType):
    print("Coloring nodes...")
    nodes = list(graph.nodes)

    if resilienceType == "degree":
        for node in nodes:
            degreeTotals.append(nx.degree(graph, node))

        degreeTotals.sort(reverse=True)

        highestDegreeTotals = []
        for i in range(num):
            highestDegreeTotals.append(degreeTotals[i])

        for node1 in nodes:
            if highestDegreeTotals.__contains__(len(graph.edges(node1))):
                color_map.append('red')
            else:
                color_map.append('blue')

    elif resilienceType == "closeness":
        for node in nodes:
            closenessTotals.append(nx.closeness_centrality(graph, node, None, True))

        closenessTotals.sort(reverse=True)

        print(closenessTotals)

        highestClosenessTotals = []
        for i in range(num):
            highestClosenessTotals.append(closenessTotals[i])
            print(closenessTotals[i])

        for node1 in nodes:
            if highestClosenessTotals.__contains__(nx.closeness_centrality(graph, node1, None, True)):
                color_map.append('red')
            else:
                color_map.append('blue')

    elif resilienceType == "betweenness":
        betweennessTotalsDict = nx.betweenness_centrality(graph, normalized=True)
        print(betweennessTotalsDict.values())

        for d in betweennessTotalsDict.values():
            betweennessTotals.append(d)

        betweennessTotals.sort(reverse=True)
        print(betweennessTotals)

        highestBetweennessTotals = []
        for i in range(num):
            highestBetweennessTotals.append(betweennessTotals[i])
            print(betweennessTotals[i])

        for node1 in nodes:
            if highestBetweennessTotals.__contains__(betweennessTotalsDict[node1]):
                color_map.append('red')
            else:
                color_map.append('blue')

    # coloring children of highest degree nodes (not working properly)

    # for n in highestEdgeTotals:
    #     for n2 in list(nx.neighbors(G, n)):
    #         if not highestEdgeTotals.__contains__(n2):
    #             color_map[n2] = 'orange'


def runResilienceTest(graph, num, resilienceType):
    graphCounter = 0
    print("Running resilience test...")
    global degreeTotals, closenessTotals, betweennessTotals, color_map, f
    numNodesOg = len(list(graph.nodes))
    f = 0.00
    nodesNumToBeRemoved = int(numNodesOg * 0.05)

    for loop in range(num):  # change number to increase the amount of times f is increased by 5%
        edges = list(graph.edges)
        nodes = list(graph.nodes)

        numNodesOg = len(list(graph.nodes))

        f += 0.05

        # nodesNumToBeRemoved = int(numNodesOg * f)  # calculate how many nodes to be removed

        numNodes = nx.number_of_nodes(graph)  # number of nodes
        graph2 = graph.copy()  # create copy of graph so nodes can be removed safetly
        removedNodes = []
        # print(len(color_map))
        betweennessTotalsDict = nx.betweenness_centrality(graph2, normalized=True)

        numNodesRemoved = 0
        for i in range(nodesNumToBeRemoved):  # run for each time a node needs to be removed
            # print("Runs: " + str(i))
            for k in range(numNodes):  # go through all nodes
                # print(str(edgeTotals[i])+" "+str(nx.degree(graph2, k)))
                # check if node exist, check if node has a high value, and checks if node was not removed before
                currentNode = list(graph2.nodes())[k]
                # print("Node: "+str(currentNode)+" degree: ", str(nx.degree(graph2, currentNode)))

                if resilienceType == "degree":
                    if graph2.has_node(currentNode) and degreeTotals[i] == int(nx.degree(graph2, currentNode)) \
                            and not removedNodes.__contains__(currentNode):
                        # print("Node: " + str(currentNode) + " with " + str(nx.degree(graph2, currentNode)) + " degree was removed")
                        numNodesRemoved = numNodesRemoved + 1
                        # print(color_map[list(graph.nodes).index(currentNode)])
                        del color_map[list(graph.nodes).index(currentNode)]  # del color associated with node to deleted
                        removedNodes.append(currentNode)  # add to list of removed nodes
                        graph.remove_node(currentNode)  # remove the node
                        break
                elif resilienceType == "closeness":
                    if graph2.has_node(currentNode) and closenessTotals[i] == nx.closeness_centrality(graph2,
                                                                                                      currentNode, None,
                                                                                                      True) \
                            and not removedNodes.__contains__(currentNode):
                        # print("Node: " + str(currentNode) + " with " + str(nx.degree(graph2, currentNode)) + " degree was removed")
                        numNodesRemoved = numNodesRemoved + 1
                        # print(color_map[list(graph.nodes).index(currentNode)])
                        del color_map[list(graph.nodes).index(currentNode)]  # del color associated with node to deleted
                        removedNodes.append(currentNode)  # add to list of removed nodes
                        graph.remove_node(currentNode)  # remove the node
                        break

                elif resilienceType == "betweenness":
                    if graph2.has_node(currentNode) and betweennessTotals[i] == betweennessTotalsDict[currentNode] \
                            and not removedNodes.__contains__(currentNode):
                        # print("Node: " + str(currentNode) + " with " + str(nx.degree(graph2, currentNode)) + " degree was removed")
                        numNodesRemoved = numNodesRemoved + 1
                        # print(color_map[list(graph.nodes).index(currentNode)])
                        del color_map[list(graph.nodes).index(currentNode)]  # del color associated with node to deleted
                        removedNodes.append(currentNode)  # add to list of removed nodes
                        graph.remove_node(currentNode)  # remove the node
                        break

        print("Number of nodes removed this pass was: ", str(numNodesRemoved))
        color_map = []
        degreeTotals = []
        closenessTotals = []
        betweennessTotals = []
        colorHighDegreeNodes(graph, 5, resilienceType)
        data = networkx.json_graph.node_link_data(graph, {"link": "edges", "source": "from", "target": "to"})
        jsonString = json.dumps(data)
        jsonFile = open("data"+str(graphCounter)+".json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()
        drawGraph(graph)
        graphCounter = graphCounter+1


if __name__ == "__main__":
    filename = input("Type in the file name of the file you want to import data from:")
    file = open(filename, encoding="utf8")
    print(filename, "successfully loaded.")
    limit = int(input("Type how many lines you want to read from the file, Type -1 to read all:"))
    faultLimit = int(input("Type how far the fault % should go (1-100):"))
    typeNum = int(input(" What type of resilience test do you want to run: 1. degree, 2. closeness, 3. betweenness"))
    resilienceType = ""
    if typeNum == 1:
        resilienceType = "degree"
    elif typeNum == 2:
        resilienceType = "closeness"
    elif typeNum == 3:
        resilienceType = "betweenness"

    total_start = time.time()  # start overall timer
    csv_reader_object = csv.reader(file)  # read file

    startNode = 0
    endNode = 0

    graph = nx.empty_graph()  # start with empty graph
    oldNode = "-1"

    print("Creating network from data imported...")
    start = time.time()  # start graph creation timer
    for line in csv_reader_object:  # go through all lines
        if limit == 0:  # unless you hit the limit set by the user
            break
        startNode = line[0]  # startNode is in the first column
        endNode = line[1]  # endNode is in the second
        if not graph.has_node(startNode):  # check if node already exists in list
            graph.add_node(startNode)
        if not graph.has_node(endNode):
            graph.add_node(startNode)
        graph.add_edge(startNode, endNode)
        if not limit == -1:
            limit = limit - 1
        # oldNode = startNode
    end = time.time()

    print("Took:", str(end - start), "seconds to create graph with", len(list(graph.nodes)), "nodes and",
          len(list(graph.edges)), "edges.")
    # G = 0
    f = 0.00
    color_map = []
    degreeTotals = []
    closenessTotals = []
    betweennessTotals = []
    highestEdgeTotals = []

    # ---------------different types of graphs-------------------------------------------
    # scale free

    # G = nx.barabasi_albert_graph(130, 4, seed=None, initial_graph=None)

    # G = nx.scale_free_graph(130)

    # exponential
    # G = nx.erdos_renyi_graph(130, 0.5)
    # G = nx.gnm_random_graph(130, 215)
    # ---------------------------------------------------------------------------------
    print(resilienceType)
    colorHighDegreeNodes(graph, 5, resilienceType)  # color before removal
    drawGraph(graph)  # draw graph before removal
    runResilienceTest(graph, int(faultLimit / 5), resilienceType)
    total_end = time.time()

    print("Test has finished.")
    print("Took: ", str(total_end - total_start), " seconds to run test.")
    # print(highestDegreeTotals)
