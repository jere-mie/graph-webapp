import networkx as nx 
import matplotlib.pyplot as plt 
import copy
import random
import math

# Functions for generating graphic sequences with k-factors

# Displays a given graph G and message with matplotlib
def displayGraph(G, message):
    ##nx.draw(G, with_labels=True)
    ##plt.suptitle(message) ##AM, 16 Dec, 2020: When is this printed ? Changing from title to suptitle printed this
    ##plt.show()
    # nx.draw(G, with_labels=True, node_color="white",edgecolors='black', font_weight='bold')
    # plt.title('Hakimi Graph') ##AM, 16 Dec, 2020: When is this printed ? Changing from title to suptitle printed this
    # plt.show()
    pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color="white", edgecolors='black' , node_size = 500, alpha = 1)
    nx.draw_networkx_labels(G, pos, {n: n for n in list(G.nodes)}, font_size=10)
    ax = plt.gca()
    for e in G.edges:
        ax.annotate("",
                     xy=pos[e[0]], xycoords='data',
                     xytext=pos[e[1]], textcoords='data',
                     arrowprops=dict(arrowstyle="-", color="0", mutation_scale=20,
                             shrinkA=12, shrinkB=12,
                             patchA=None, patchB=None,
                             #connectionstyle="arc3,rad=rrr".replace('rrr',str(0.3*e[2]+1)
                             connectionstyle="arc3,rad=0.0"
                             #),
                         ),
                     )
    plt.title("k-factor") ##AM, 16 Dec, 2020: When is this printed ? Changing from title to suptitle printed this
    plt.axis('off')
    plt.show()

# Generates a degree sequence with given size, max val, min val
def GenerateDegrees(n, minDeg, maxDeg):
    degSeq = []
    sumDeg = 0
    for i in range(n-1):
        x = random.randint(minDeg, maxDeg)
        degSeq.append(x)
        sumDeg = sumDeg + x
    if sumDeg % 2 == 0:
        if minDeg % 2 == 0:
            degSeq.append(minDeg)
        else:
            degSeq.append(minDeg + 1)
    else:
        if minDeg % 2 == 0:
            degSeq.append(minDeg + 1)
        else:
            degSeq.append(minDeg)
    degSeq=sorted(degSeq, reverse=True)
    return degSeq

# ***** Between here and the bottom stars was implemented June 2024 - Lucas Sarweh

# Generates a graphic sequence with connected k-factors based on
# trial and error heuristic in section 2
# Params:
# k - an integer
# a, b - integers
# Restrictions:
# k >= 2
# a >= b > 0
# WIP: k < mySeq[0] <= a, otherwise the graph is realizable, but a k-factor will not be found
def generateSequenceConnectedTrialError(k, a, b):
    # WIP

    # Check restrictions
    if k < 2 or a < b or b < 1:
        print("Requirements not met")
        return 0

    # Generate (randomly) a sequence with n longer than l and sums to be even,
    # this ensures the sequence (d) is graphic
    # n = |d| ≥ (a + b + 1)^2/4b = l
    n = nSetToL(a, b) # This only gives minimum n >= l, might change to be random number between nSetToL and some greater bound

    mySeq = []

    # Loop through this block until we have found a good sequence
    while(True):
        # Generate random sequence
        mySeq = GenerateDegrees(n, b, a)

        # Ensure the sequence d - k is also graphic
        # Using Σ(i=1 to k) di <= k(k - 1)  + Σ(i=k+1 to n) min(k, di)
        # Construct d - k sequence
        mySeqMinK = []
        for i in mySeq:
            if i - k > 0:
                mySeqMinK.append(i - k)
        
        if checkEGI(mySeqMinK) == False:
            # Else choose another sequence
            continue

        # Check if it has a connected k-factor
        # for each s < n/2
        # Σ(i=1 to s) d[i] < s(n - s - 1) + Σ(i=0 to s-1) d[n-i]
        # must hold
        if checkConnectedKFactor(mySeq) == False:
            # Else generate a new sequence and try again
            continue
    
        # All checks passed exit loop
        break
        
    # return sequence
    return mySeq

# Generates an n set to l using
# n = |d| ≥ (a + b + 1)^2/4b = l
def nSetToL(a, b):
    # Use ceiling to ensure an integer >= l
    return math.ceil((math.pow(a + b + 1, 2))/(4 * b))

# Ceiling division
def ceildiv(a, b):
    return -(a // -b)

# Checks if a sequence is graphic using
# the Erdos and Gallai Inequalities
# Σ(i=1 to k) di <= k(k - 1)  + Σ(i=k+1 to n) min(k, d[i])
def checkEGI(seq):
    n = len(seq)
    sum = 0
    # Firstly, must sum to an even number
    for i in seq:
        sum += i
    
    # Not even sum, automatically not graphic
    if sum % 2 != 0:
        return False
    
    sum = 0

    # Σ(i=1 to k) d[i] <= k(k - 1)  + Σ(i=k+1 to n) min(k, d[i])

    # For each k, 1 <= k <= n
    for k in range(1, n+1):
        # k(k - 1)
        sumRight = k * (k - 1)
        sumLeft = 0
        # + Σ(i=k+1 to n) min(k, di)
        for i in range(k+1, n+1):
            # [i - 1] used because index starts at 0 here, but 1 in paper
            sumRight += min(k, seq[i - 1])
        # Sum Left side of inequality Σ(i=1 to k) d[i]
        for i in range(1, k+1):
            sumLeft += seq[i - 1]
        
        # Check if equality holds sumLeft <= sumRight
        if sumLeft > sumRight:
            # EGI does not hold, not a graphic sequence
            return False        
    
    # All values of k passed, it is graphic
    return True

# This checks if a degree sequence has a connected k-factor using
# Σ(i=1 to s) d[i] < s(n - s - 1) + Σ(i=0 to s-1) d[n-i]
# for each s < n/2 from (2) in section 2
def checkConnectedKFactor(seq):
    n = len(seq)
    # For each s < n/2
    for s in range(1, ceildiv(n, 2)):
        sumLeft = 0
        # s(n - s - 1)
        sumRight = s*(n - s - 1)
        
        # Σ(i=1 to s) d[i]
        for i in range(1, s+1):
            sumLeft += seq[i - 1]
        
        # + Σ(i=0 to s-1) d[n-i]
        for i in range(s):
            sumRight += seq[n - i - 1]
        
        # sumLeft < sumRight must hold
        if sumLeft >= sumRight:
            # It has no connected k-factor
            return False

    # All values of s pass, has connected k-factor
    return True

# Generates a graphic sequence with a connected
# k-factor from section 2 page 3, on removing trial and error
# Params:
# k - an integer, may not be required
# a, b - integers
# Restrictions:
# a >= b > 0
# 2 != a - b
def generateSequenceConnected(a, b):
    # WIP

    # Check restrictions
    if a < b or b <= 0 or a - b == 2:
        print("Requirments not met")
        return 0

    # Find length of sequence d
    # n > max{4/(2 + b − a), (a + b + 1)^2/4b}
    # so set n to max + 1
    n = findMinN(a, b)

    # Randomly Generate sequence with obtained n keeping in mind the restictions
    # of a >= d >= b > 0 and ensure sequence sums to even
    mySeq = GenerateDegrees(n, b, a)


    # Return that sequence
    return mySeq

# Find minumum possible length of the sequence
# n > max{4/(2 + b − a), (a + b + 1)^2/4b}
# Restrictions:
# a - b != 2
def findMinN(a, b):
    # Calculate max
    n = max(4 / (2 + b - a), math.pow((a + b + 1), 2) / (4 * b))
    # Ensure n is greater and not equal
    n = math.floor(n) + 1 # Only python 3 floor() returns int, python 2.* returns float

    return n

# This will only generate graphic sequences with disconnected s-factors
# Sequence will be of the form (n-1, ..., n-1, x, ..., x, s, ..., s)
# x lies in the range: 2s <= x <= n-s-1
# Requirements:
# n -> Must be even
# k -> k = s < n/2
# 3k + 1 <= n
def generateSequenceDisconnected(n, k):
    # WIP
    # Assume n is even
    if n % 2 != 0:
        print("n must be even, requirement not met")
        return None
    # Ensure sufficient distance between k and n
    if 3*k + 1 > n:
        print("3k + 1 <= n, requirement not met")
        return None
    # fix an s < n/2
    if k < (n / 2):
        s = k
    else:
        print("k = s < n/2, requirement not met")
        return None

    mySeq = []
    # Random value for x between its restrictions
    x = random.randint(2*s, n - s - 1)
    
    # Make [n - 1] * s entries at the front, [s] * s entries at the end, and [x] * n - 2s middle entries
    for i in range(s):
        mySeq.append(n - 1)
    for i in range(n - 2*s):
        mySeq.append(x)
    for i in range(s):
        mySeq.append(s)

    return mySeq


# *****

# this function implements the Hakimi-Havel algorithm
# Params:
# n -> degree sequence length
# degSeq - > The degree sequence
# G -> Output graph
def constructGraph(n, degSeq, G):
    print ("n=", n)
    #Initialize
    nodeList=[]
    for i in range(0,n):
        nodeList.append(i)
    print (nodeList)
    resDegList=[]
    resDegList=copy.deepcopy(degSeq) #AM, 16 Dec., 2020: Why use deepcopy here ? 
    DS=[] #AM, 16 Dec., 2020:  What's this for ? this helps in maintaining the degree-vertex label association
    #for i in range(n-1,-1,-1):
    for i in range(0, n):
        DS.append((resDegList[i][0],resDegList[i][1]))
    #sort in decreasing order with respect to the vertex degrees
    DS=sorted(DS,key=lambda x:x[1], reverse=True) #syntax from W3Schools.py: sorted(iterable, key=key, reverse=reverse)
                                                  #lambda x: x[1] is an anonymous function returning the second element 
                                                  # of [Nodes[i],Degrees[i]] to be used as the key with respect to which to sort
        
    print("Initial DS=",DS)
    #Extract residual degree and node-label lists
    nodeList = [x[0] for x in DS] #AM, 16 Dec., 2020: label list
    resDegList = [x[1] for x in DS] #AM, 16 Dec., 2020: degree list

    rightIndex = n-1; #the algorithm is about managing this right index correctly
    #A leftToRightIndex is used to reduce vertex degrees, from 0 going right and is bounded above by rightIndex
  
    while (resDegList[0] > 0 and resDegList[0] <= rightIndex):
        #right-moving index 
        #k=resDegList[0]
        k=random.choice(nodeList)
        print("Chosen node : ",k)
        for i in range(0,len(DS)):
            if k==DS[i][0]:
                n=DS.pop(i)
                DS.insert(0,n)
                break
        #print("DS after picking random node: ",DS)
        nodeList = [x[0] for x in DS] #AM, 16 Dec., 2020: label list
        resDegList = [x[1] for x in DS] #AM, 16 Dec., 2020: degree list
        for m in range(0,len(resDegList)):
            if resDegList[m]!=k:
                break
        random.shuffle(nodeList[0:m])
        
        leftToRightIndex = 1 
             
        #move right, reduce degrees and add edges
        while (resDegList[0] > 0 and leftToRightIndex <= rightIndex):
            G.add_edge(nodeList[0],nodeList[leftToRightIndex])
            print("Introducing edge between ", nodeList[0]," and ",nodeList[leftToRightIndex])
            resDegList[0] =resDegList[0] - 1
            resDegList[leftToRightIndex] = resDegList[leftToRightIndex] - 1
            leftToRightIndex += 1

    #now merge degree and label lists
        zippy = zip(nodeList, resDegList) 
        DS = list(zippy)
                 
        #resort DS 
        DS=sorted(DS,key=lambda x:x[1], reverse=True)
        print("DS=",DS) #for test purposes
             
        #Extract residual degree and node-label lists for the next round of edge additions
        nodeList = [x[0] for x in DS] #AM, 16 Dec., 2020: label list
        resDegList = [x[1] for x in DS] #AM, 16 Dec., 2020: degree list

        #move rightIndex left to the index of the first non-zero residual degree
        while (rightIndex > 0 and resDegList[rightIndex] == 0):
            rightIndex -= 1

    #outside the outermost while
    if (resDegList[0] > rightIndex): #this happen when the sequence is not graphical
       flag = 0
    else: #both resDegList[0] and rightIndex are 0
       flag = 1
    return flag

def mergeVertex(DS, vertex, n):
    while(DS[n][1] > vertex[1]): # Loop till the item in array is greater than the vertex
        n = n-1
        if (n < 0):
            break
    DS.insert(n+1, vertex) #Insert the vertex after the first item smaller than the vertex
    return DS

def removeMultipleEdges(G):
    multipleEdge = [edge for edge in G.edges if edge[2]>0] #Get all the multiedge in the graph
    for idx, me in enumerate(multipleEdge):
        if not G.has_edge(me[0], me[1], 1):
            continue
        if idx+1 < len(multipleEdge):
            G.remove_edge(multipleEdge[idx][0], multipleEdge[idx][1])
            G.remove_edge(multipleEdge[idx+1][0], multipleEdge[idx+1][1])
            G.add_edge(multipleEdge[idx][0], multipleEdge[idx+1][0])
            G.add_edge(multipleEdge[idx][1], multipleEdge[idx+1][1])
            break
        for edge in G.edges:
            if me[0] != edge[0] and me[0] != edge[1] and me[1] != edge[0] and me[1] != edge[1]: #check if the edge is not switching to itself
                if G.has_edge(me[0], edge[0]) == False and G.has_edge(me[1], edge[1]) == False: #check if the new edge created will become a multi edge and draw if it doesnt
                    G.remove_edge(me[0], me[1])
                    G.remove_edge(edge[0], edge[1])
                    G.add_edge(me[0], edge[0])
                    G.add_edge(me[1], edge[1])
                    # print(me, edge)
                    break
                if G.has_edge(me[0], edge[1]) == False and G.has_edge(me[1], edge[0]) == False:  #check if the new edge created will become a multi edge and draw if it doesnt
                    G.remove_edge(me[0], me[1])
                    G.remove_edge(edge[0], edge[1])
                    G.add_edge(me[0], edge[1])
                    G.add_edge(me[1], edge[0])
                    # print(me,edge)
                    break
    # print (multipleEdge)

def createAdjacencyMatrix(G, M, n):
    for i in range(n):
        dimension1 = []
        for j in range(n):
            dimension1.append(0)
        M.append(dimension1)
    for edge in G.edges: #parse through the edge in the graph and assign 1 in the matrix
        M[edge[0]][edge[1]] = 1
        M[edge[1]][edge[0]] = 1

def superImposeGraph(M1, M2, n):
    M=[]
    for i in range(n):
        temp = []
        for j in range(n):
            if M1[i][j] == 1 and M2[i][j] == 1: #assign 1 when edge is found in both matrix
                temp.append(1)
            else:
                temp.append(0)
        M.append(temp)
    return M

# def switchEdgesAfterSuperImposing(G1, M, n):
#     for i in range(n):
#         for j in range(i+1,n):
#             if M[i][j] == 1:
#                 print("temporary edge", i, j)
#                 G1.add_edge(i,j) #temporarily add edge which are common in both graphs
#     print("edges before", G1.edges)
#     removeMultipleEdges(G1) # remove multiple edges(only the temporarily added edges will be multiple edges)
#     print("edges after", G1.edges)
#     for i in range(n):
#         for j in range(i+1,n):
#             if M[i][j] == 1:
#                 G1.remove_edge(i,j) # remove the temporarily added edges

def complementGraph(M, n):
    for i in range(n):
        for j in range(n):
            if M[i][j] == 0:
                M[i][j] = 1
            else:
                M[i][j] = 0

def removeSuperimposingEdges(G1, G2, M, n):
    edgeArr = []
    for i in range(n):
        for j in range(i+1,n):
            if M[i][j] == 1:
                print("temporary edge", i, j)
                edgeArr.append([i,j])
    for superEdge in edgeArr:
        for edge in G2.edges:
            if superEdge[0] != edge[0] and superEdge[0] != edge[1] and superEdge[1] != edge[0] and superEdge[1] != edge[1]:
                if (G1.has_edge(superEdge[0], edge[1]) == False and G1.has_edge(superEdge[1], edge[0]) == False) and (G2.has_edge(superEdge[0], edge[1]) == False and G2.has_edge(superEdge[1], edge[0]) == False):
                    if G2.has_edge(superEdge[0], superEdge[1]) == True:
                        G2.remove_edge(superEdge[0], superEdge[1])
                        G2.remove_edge(edge[0], edge[1])
                        G2.add_edge(superEdge[0], edge[1])
                        G2.add_edge(superEdge[1], edge[0])
                    break
                if (G1.has_edge(superEdge[0], edge[0]) == False and G1.has_edge(superEdge[1], edge[1]) == False) and (G2.has_edge(superEdge[0], edge[0]) == False and G2.has_edge(superEdge[1], edge[1]) == False):
                    if G2.has_edge(superEdge[0], superEdge[1]) == True:
                        G2.remove_edge(superEdge[0], superEdge[1])
                        G2.remove_edge(edge[0], edge[1])
                        G2.add_edge(superEdge[0], edge[0])
                        G2.add_edge(superEdge[1], edge[1])
                    break

def createGraphFromMatrix(G, M, n):
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(i+1, n): # only create edge from i+1 as rest are repeated in matrix
            if M[i][j] == 1:
                G.add_edge(i,j)

def subtractGraph(M2, M1, n):
    M = []
    for i in range(n):
        temp=[]
        for j in range(n):
            if M2[i][j] == 1 and M1[i][j] == 1: # remove edge if found in both
                temp.append(0)
            else:
                temp.append(M2[i][j]) # add edge only if it is present in M2
        M.append(temp)
    return M
