#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun 25 Dec 2020
accessed: 24 Feb, 2023

@author: asish mukhopadhyay, amreeth nagarajan

Version: 2

Specifics about this version: 
In this version, randomly selected nodes are selected for saturation 
instead of the node with the highest degree (second degree criteria: 
lowest label). The changes are only made on the function containing 
module.

"""

import networkx as nx
import matplotlib.pyplot as plt
import copy
import random


def displayGraph(G):
    nx.draw(G, with_labels=True, node_color="white",
            edgecolors='black', font_weight='bold')
    # AM, 16 Dec, 2020: When is this printed ? Changing from title to suptitle printed this
    plt.suptitle('A Graphic Realization')
    # inside the drawing area
    plt.show()

# this function implements the Hakimi-Havel algorithm


def constructGraph(n, degSeq, G):
    print("n=", n)
    nodeList = []
    for i in range(0, n):
        nodeList.append(i)
    # print (nodeList)

    resDegList = copy.deepcopy(degSeq)
    # deepcopy so that changes in resDegList doesn't affect degSeq

    DS = []
    # DS is a 2D that helps maintain the degree-vertex label association
    for i in range(0, n):
        DS.append((nodeList[i], resDegList[i]))

    # sort in decreasing order with respect to the vertex degrees
    DS = sorted(DS, key=lambda x: x[1], reverse=True)
    print("Initial DS=", DS)

    # Extract residual degree and node-label lists
    nodeList = [x[0] for x in DS]  # Node label list
    resDegList = [x[1] for x in DS]  # Degree list

    rightIndex = n-1
    # The algorithm is about managing this right index correctly
    # A leftToRightIndex is used to reduce vertex degrees, from 0
    # going right and is bounded above by rightIndex

    while (resDegList[0] > 0 and resDegList[0] <= rightIndex):

        print("\n--------------------------\n")
        print("Right index is ", rightIndex)
        print("Res deg list: ", resDegList)
        print("DS: ", DS)

        # Collect the non-zero nodes
        eligibleNodes = []
        for i in range(0, len(resDegList)):
            if resDegList[i] != 0:
                eligibleNodes.append(nodeList[i])

        # Choose a node randomly
        k = random.choice(eligibleNodes)
        print("Chosen node : ", k)

        # Inserting k at the start of the list
        for i in range(0, len(DS)):
            if k == DS[i][0]:
                n = DS.pop(i)
                DS.insert(0, n)
                break
        print("DS after picking random node: ", DS)

        nodeList = [x[0] for x in DS]  # updated label list
        resDegList = [x[1] for x in DS]  # updated degree list

        leftToRightIndex = 1
        print(" and leftToRightIndex is ", leftToRightIndex)

        # move right, reduce degrees and add edges
        while (resDegList[0] > 0 and leftToRightIndex <= rightIndex):
            G.add_edge(nodeList[0], nodeList[leftToRightIndex])
            # comment this line to stop intermediate displays of partial graphs
            # displayGraph(G)
            print("Introducing edge between ",
                  nodeList[0], " and ", nodeList[leftToRightIndex])
            resDegList[0] = resDegList[0] - 1
            resDegList[leftToRightIndex] = resDegList[leftToRightIndex] - 1
            leftToRightIndex += 1
            print(" and leftToRightIndex is ", leftToRightIndex)

        # Update DS by merging the updated lists
        zippy = zip(nodeList, resDegList)
        DS = list(zippy)

        # resort DS
        DS = sorted(DS, key=lambda x: x[1], reverse=True)
        print("DS=", DS)

        nodeList = [x[0] for x in DS]  # sorted label list
        resDegList = [x[1] for x in DS]  # sorted degree list

        print("rightIndex: ", rightIndex)
        # move rightIndex left to the index of the first non-zero residual degree
        while (rightIndex > 0 and resDegList[rightIndex] == 0):
            rightIndex -= 1

        print("new rightIndex: ", rightIndex)
    # outside the outermost while
    if (resDegList[0] > rightIndex):
        # this happen when the sequence is not graphical
        print("resDegList[0] is ", resDegList[0],
              "AND right index is ", rightIndex)
        flag = 0
    else:  # both resDegList[0] and rightIndex are 0
        flag = 1

    return flag
