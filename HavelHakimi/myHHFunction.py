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


def displayGraph(G):
    nx.draw(G, with_labels=True, node_color="white",
            edgecolors='black', font_weight='bold')
    plt.suptitle('A Graphic Realization')
    plt.show()


def constructGraph(n, degSeq):

    # Sort the list in non-increasing order
    degSeq = sorted(degSeq, reverse=True)

    # Check if the sum of degrees is even
    if sum(degSeq) % 2 != 0:
        return False

    # Create empty graph with n nodes
    G = nx.Graph()
    G.add_nodes_from(range(n))

    # Keep performing the operations until one
    # of the stopping condition is met
    while True:

        # Check if all the degrees are zero
        if all(deg == 0 for deg in degSeq):
            return G

        # Check if the largest degree is greater
        # than the number of remaining vertices
        if degSeq[0] > len(degSeq) - 1:
            return nx.Graph()  # Returns an empty graph

        # Connect the node with largest degree
        # to the next v highest degree nodes
        v = degSeq[0]
        degSeq = [deg - 1 for deg in degSeq[1:v+1]] + degSeq[v+1:]
        G.add_edges_from([(0, i) for i in range(1, v+1)])
        degSeq[0] = v - len(list(G.adj[0]))

# Function to be passed to back end


def graph_exists(n, degSeq):

    # Keep performing the operations until one
    # of the stopping condition is met
    while True:

        # Sort the list in non-decreasing order
        degSeq = sorted(degSeq, reverse=True)

        # Check if all the elements are equal to 0
        if degSeq[0] == 0 and degSeq[-1] == 0:
            return True

        # Store the first element in a variable
        # and delete it from the list
        v = degSeq[0]
        degSeq = degSeq[1:]

        # Check if enough elements
        # are present in the list
        if v > len(degSeq):
            return False

        # Subtract first element from next v elements
        for i in range(v):
            degSeq[i] -= 1

            # Check if negative element is
            # encountered after subtraction
            if degSeq[i] < 0:
                return False
