# constructDirectedGraph handles 4 cases for proving the sufficiency
# We maintain variable r for getting one vertex at a time from the right set and saturate that vertex using the four cases.
# If v_r do not get saturated in these 4 cases, then the graph is not realizable as the inequality is violated.
# When the last vertex is r all the vertices have the outdegrees exhausted except for the vertex r. 

import networkx as nx 


def displayGraph(G):
    pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color="white", edgecolors='black' , node_size = 500, alpha = 1)
    nx.draw_networkx_labels(G, pos, {n: n for n in list(G.nodes)}, font_size=10)
    # nx.draw_networkx_edges(G, pos, edge_color="black", arrows=True, connectionstyle="arc3, rad = 0.3")
    ax = plt.gca()
    for e in G.edges:
        ax.annotate("",
                    xy=pos[e[0]], xycoords='data',
                    xytext=pos[e[1]], textcoords='data',
                    arrowprops=dict(arrowstyle="<|-", color="0", mutation_scale=20,
                            shrinkA=12, shrinkB=12,
                            patchA=None, patchB=None,
                            connectionstyle="arc3,rad=rrr".replace('rrr',str(0.3*(e[2]+1))
                            ),
                        ),
                    )
    plt.title('Directed Graph')
    plt.axis('off')
    plt.show()

def constructDirectedGraph(G, degList, n):
    degreePairList = []
    # create a list of degree pairs
    for i in range(n):
        degreePairList.append([int(degList[i][0].split(',')[0]), int(degList[i][0].split(',')[1]), degList[i][1]])
        G.add_node(degList[i][1])
    leftDegSet = []
    rightDegSet = []
    rightDegSet = degreePairList

    iterations = [] # FINAL JSON
    
    # TEMP VARIABLES FOR ABOVE JSON
    flag = False
    addEdge = []
    delEdge = []

    while len(rightDegSet) > 0:
        r = rightDegSet.pop(0)
        # print("Vertex assigned to Vr = " + str(r[2]))
        # case 0
        for item in rightDegSet:
            if r[0] == 0:
                break
            else:
                if item[1] > 0:
                    # print("Case 0")
                    r[0] = r[0] - 1
                    item[1] = item[1] - 1
                    G.add_edge(r[2], item[2])
                    addEdge.append([r[2], item[2]])
                    flag = True;
        for item in leftDegSet:
            if r[0] == 0:
                break
            else:
                if item[1] > 0:
                    print("Case 0")
                    r[0] = r[0] - 1
                    item[1] = item[1] - 1
                    G.add_edge(r[2], item[2])
                    addEdge.append([r[2], item[2]])
                    flag = True
        if flag:
            iterations.append({
                'case': 0,
                'addEdge': addEdge,
                'delEdge': delEdge
            })
            addEdge = []
            delEdge = []
            flag = False
        
        # case 1
        temp = -1
        while r[0] > 0 and r[1] > 0:
            temp = r[0]
            for leftItem in leftDegSet:
                # temp = -1
                if r[1] <= 0 or r[0] <= 0:
                    break
                # temp = r[0]
                # print(leftItem)
                outEdgeList = G.out_edges(leftItem[2])
                for outEdge in outEdgeList:
                    # print(rightDegSet)
                    rightSet = [row[2] for row in rightDegSet]
                    leftSet = [row[2] for row in leftDegSet]
                    if len(rightDegSet)> 0 and outEdge[1] in rightSet and not G.has_edge(r[2], outEdge[1]):
                        # print("Case 1")
                        G.remove_edge(outEdge[0], outEdge[1])
                        delEdge.append([outEdge[0], outEdge[1]])
                        r[0] = r[0] - 1
                        r[1] = r[1] - 1
                        G.add_edge(outEdge[0], r[2])
                        addEdge.append([outEdge[0], r[2]])
                        G.add_edge(r[2], outEdge[1])
                        addEdge.append([r[2], outEdge[1]])
                        # print(outEdge[0], '->', r[2], ',', r[2], '->', outEdge[1])
                        flag = True
                        break
                    elif len(leftDegSet)> 0 and outEdge[1] in leftSet and not G.has_edge(r[2], outEdge[1]):
                        # print("Case 1")
                        G.remove_edge(outEdge[0], outEdge[1])
                        delEdge.append([outEdge[0], outEdge[1]])
                        r[0] = r[0] - 1
                        r[1] = r[1] - 1
                        G.add_edge(outEdge[0], r[2])
                        addEdge.append([outEdge[0], r[2]])
                        G.add_edge(r[2], outEdge[1])
                        addEdge.append([r[2], outEdge[1]])
                        # print(outEdge[0], '->', r[2], ',', r[2], '->', outEdge[1])
                        flag = True
                        break
            if temp == r[0]:
                break
        if flag:
            iterations.append({
                'case': 1,
                'addEdge': addEdge,
                'delEdge': delEdge
            })
            addEdge = []
            delEdge = []
            flag = False

        # case 2

        temp = -1
        while r[0] > 0:
            temp = r[0]
            for leftItem in leftDegSet:
                if r[0] <= 0:
                    break
                outEdgeList = G.out_edges(leftItem[2])
                for outEdge in outEdgeList:
                    tempList = list(filter(lambda x: x[1] > 0 and not G.has_edge(outEdge[0], x[2]), rightDegSet))
                    if len(tempList) > 0:
                        rightSet = [row[2] for row in rightDegSet]
                        if len(rightDegSet)>0 and outEdge[1] in rightSet and not G.has_edge(r[2], outEdge[1]):
                            # print("Case 2")
                            G.remove_edge(outEdge[0], outEdge[1])
                            delEdge.append([outEdge[0], outEdge[1]])
                            r[0] = r[0] - 1
                            G.add_edge(outEdge[0], tempList[0][2])
                            addEdge.append([outEdge[0], tempList[0][2]])
                            tempList[0][1] = tempList[0][1]-1
                            G.add_edge(r[2], outEdge[1])
                            addEdge.append([r[2], outEdge[1]])
                            flag = True
                            break
                    # else:
                    #     tempList = list(filter(lambda x: x[1] > 0 and not G.has_edge(outEdge[0], x[2] and x != leftItem), leftDegSet))
                    #     if len(tempList) > 0:
                    #         if len(leftDegSet)>0 and outEdge[1] in leftDegSet[:,2] and not G.has_edge(r[2], outEdge[1]):
                    #             print("Case 2")
                    #             G.remove_edge(outEdge[0], outEdge[1])
                    #             r[0] = r[0] - 1
                    #             G.add_edge(outEdge[0], tempList[0][2])
                    #             G.add_edge(r[2], outEdge[1])
                    #             break
            if temp == r[0]:
                break

        if flag:
            iterations.append({
                'case': 2,
                'addEdge': addEdge,
                'delEdge': delEdge
            })
            addEdge = []
            delEdge = []
            flag = False
        # case 3

        temp = -1
        while r[0] > 0:
            temp = r[0]
            for leftItem in leftDegSet:
                if r[0] <= 0:
                    break
                outEdgeList = G.out_edges(leftItem[2])
                for outEdge in outEdgeList:
                    tempList = list(filter(lambda x: x[1] > 0 and not G.has_edge(outEdge[0], x[2]) and outEdge[0] != x[2], leftDegSet))
                    if len(tempList) > 0:
                        rightSet = [row[2] for row in rightDegSet]
                        leftSet = [row[2] for row in leftDegSet]
                        if len(rightDegSet)>0 and outEdge[1] in rightSet and not G.has_edge(r[2], outEdge[1]):
                            # print("Case 3")
                            G.remove_edge(outEdge[0], outEdge[1])
                            delEdge.append([outEdge[0], outEdge[1]])
                            r[0] = r[0] - 1
                            G.add_edge(outEdge[0], tempList[0][2])
                            addEdge.append([outEdge[0], tempList[0][2]])
                            tempList[0][1] = tempList[0][1]-1
                            G.add_edge(r[2], outEdge[1])
                            addEdge.append([r[2], outEdge[1]])
                            # print('removed: ', outEdge[0], '->', outEdge[1])
                            # print('added: ', outEdge[0], '->', tempList[0][2], ',', r[2], '->', outEdge[1])
                            flag = True
                            break
                        elif(len(leftDegSet)>0 and outEdge[1] in leftSet and not G.has_edge(r[2], outEdge[1])):
                            # print("Case 3")
                            G.remove_edge(outEdge[0], outEdge[1])
                            delEdge.append([outEdge[0], outEdge[1]])
                            r[0] = r[0] - 1
                            G.add_edge(outEdge[0], tempList[0][2])
                            addEdge.append([outEdge[0], tempList[0][2]])
                            tempList[0][1] = tempList[0][1]-1
                            G.add_edge(r[2], outEdge[1])
                            addEdge.append([r[2], outEdge[1]])
                            # print('removed: ', outEdge[0], '->', outEdge[1])
                            # print('added: ', outEdge[0], '->', tempList[0][2], ',', r[2], '->', outEdge[1])
                            flag = True
                            break
            if temp == r[0]:
                break

        if flag:
            iterations.append({
                'case': 3,
                'addEdge': addEdge,
                'delEdge': delEdge
            })
            addEdge = []
            delEdge = []
            flag = False

        if r[0] > 0:
             return []
        else:
            leftDegSet.append(r)
        #print(leftDegSet, rightDegSet)
        return iterations

def greaterThan(item1, item2):
    vertex1 = item1.split(',')
    vertex2 = item2.split(',')
    if(vertex1[0] == vertex2[0]):
        if(int(vertex1[1]) > int(vertex2[1])):
            return 1
        else:
            return -1
    if(int(vertex1[0])>int(vertex2[0])):
        return 1
    else:
        return -1

def sortVertices(arr, n):
    for i in range(n-1):
        for j in range(n-i-1):
            if (greaterThan(arr[j][0],arr[j+1][0]) < 0):
                temp = arr[j+1]
                arr[j+1] = arr[j]
                arr[j] = temp
    return arr
