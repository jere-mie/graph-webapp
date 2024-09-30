import os
import json
import sys
from flask import Flask, abort, jsonify, render_template, request
from graph_algos.chordal_graph_interface import generateCG
from graph_algos import FR_DirectedGraphGeneration as kw
from graph_algos import NetworkResilience as nr
from graph_algos import HavelHakimi as hh
from graph_algos import kfactor as kf
from graph_algos import generationBasedOnSeacrest as sc
import networkx as nx
import random

"""
Setup
"""

# getting config details
with open('config.json') as f:
    config = json.load(f)

# initializing Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = config['secret_key']

"""
Page routes
"""

@app.route('/home', methods=['GET'])
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/graph', methods=['GET'])
def graph():
    return render_template('graph.html')

@app.route('/graphtemplate', methods=['GET'])
def graphtemplate():
    return render_template('graph-template.html')

@app.route('/graph/<name>', methods=['GET'])
def graphapp(name):
    if name not in {"chordal-graph-k-chromatic", "unified-chordal-graph", "random-graph-evolution", "binomial-graph-evolution", "network-resilience-test", 'fulkerson-ryser', 'havel-hakimi', 'k-factor'}:
        abort(404)
    return render_template(f'{name}.html')

"""
Error handlers
"""

@app.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400

"""
API endpoints
"""

# endpoint for chordal graph
@app.route('/api/unified-graph', methods=['GET'])
def chordal():
    nodes = int(request.args.get('nodes'))
    edges = int(request.args.get('edges'))
    deletion_start = request.args.get('deletionstart')
    complete_graph = {}

    if not nodes:
        abort(400, description="Node(s) not found")
    if not edges:
        abort(400, description="Edge(s) not found")
    if nodes < 1:
        abort(400, description="nodes < 1")
    if edges < 1:
        abort(400, description="edges < 1")

    if deletion_start == 'true' and int(nodes) <= 50:

        complete_graph["nodes"] = []
        for i in range(nodes):
            complete_graph["nodes"].append({"id": i})
        complete_graph["lastNodeId"] = nodes - 1
        complete_graph["links"] = []
        for i in range(nodes):
            for j in range(i, nodes):
                if i != j:
                    complete_graph["links"].append({"source": i, "target": j})

    def adjList2linkPairs(adjlist):
        keys = adjlist.keys
        graph = {}
        nodeobjects = [{id: key} for key in keys]
        graph["nodes"] = nodeobjects
        lastNodeID = len(keys)-1
        graph["lastNodeID"] = lastNodeID
        linkpairs = []

        for i in range(len(keys)):
            key = keys[i]
            for j in len(adjlist[key]):
                n0 = int(key)
                n1 = adjlist[key][j]

                pair = {"source": n0, "target": n1}
                if pair not in linkpairs:
                    linkpairs.append(pair)
        graph["links"] = map(jsonify, linkpairs)

    graphs = generateCG(nodes, edges, deletion_start)
    map(adjList2linkPairs, graphs)
    if deletion_start and nodes <= 50:
        graphs[0] = complete_graph
    return jsonify(graphs)

# we are receiving two lists from frontend, indegrees and outdegrees, whose elements should be seperated by a comma in the request
@app.route('/api/fulkerson', methods=['GET'])
def fulkersonryser():
    G = nx.MultiDiGraph()
    indegrees = str(request.args.get("indegrees")).split(",")
    outdegrees = str(request.args.get("outdegrees")).split(",")
    num_nodes = len(outdegrees)
    print("n: ", num_nodes)
    print("ind: ", indegrees)
    print("outd: ", outdegrees)
    degList = []

    for i in range(num_nodes):
        degValue = [str(outdegrees[i]) + "," + str(indegrees[i]), i+1]
        degList.append(degValue)
        print("dv: ", degValue)

    sortedDegList = kw.sortVertices(degList, num_nodes)
    return kw.constructDirectedGraph(G, sortedDegList, num_nodes)

# we are receiving one list from frontend, a list of node degrees
@app.route('/api/havelhakimi', methods=['GET'])
def havelhakimi():
    degree_list_input = request.args.get("degreelist")
    print(degree_list_input)
    degree_list_input = degree_list_input.split(",")
    print(degree_list_input)
    degreeList = [int(x) for x in degree_list_input]

    graph = hh.constructGraph(len(degreeList), degreeList, nx.Graph())
    return jsonify(graph)

@app.route('/api/k-factor', methods=['GET'])
def kfactor():
    degree_list_input = request.args.get("degreelist")
    print(degree_list_input)
    degree_list_input = degree_list_input.split(",")
    print(degree_list_input)
    degreeList = [int(x) for x in degree_list_input]\


    k = degreeList.pop()
    print(k)
    n = len(degreeList)

    graphs = kf.constructGraph(degreeList, n, k)

    return jsonify(graphs)

@app.route('/api/give_sequence', methods=['GET'])
def give_sequence():
    give_type = request.args.get("type")
    if(give_type == 'connected'):
        # Needs to be randomized numbers
        a = random.randint(1, 25) # second param sets the max degree in the sequence
        b = random.randint(1, a)

        response_seq = sc.generateSequenceConnected(a, b)

        # Find one of the k's that fit
        notfound = True
        while(notfound):
            # k < largest degree
            k = random.randint(2, response_seq[0] - 1)

            # Ensure the sequence has this k-factor
            mySeqMinK = []
            for i in response_seq:
                if i - k > 0:
                    mySeqMinK.append(i - k)
            
            if(sc.checkEGI(mySeqMinK)):
                # k found
                notfound = False
        
        response_seq.append(k)
        return jsonify(response_seq)
    elif(give_type == 'disconnected'):
        # Needs to be randomized
        # n must be even and atleast 7 (which implies 8)
        n = random.randrange(8, 25, 2) # second param sets the max degree in the sequence
        # Usually you fix a k = s < n/2, but 2s <= x <= n-s-1
        k = random.randint(2, int((n-1)/3))
        response_seq = sc.generateSequenceDisconnected(n, k)
        response_seq.append(k)
        return jsonify(response_seq)
    # should never reach here
    print("BAD****************")
    return -1
        

@app.route('/api/network_resilience', methods=['GET'])
def network_resilience():
    inputfile = request.args.get("file")
    num_nodes = request.args.get("num_nodes")
    fault_percent = request.args.get("fault_percent")
    resilience_type = request.args.get("resilience_type")

    def adjList2linkPairs(adjlist):
        keys = adjlist.keys
        graph = {}
        nodeobjects = [{id: key} for key in keys]
        graph["nodes"] = nodeobjects
        lastNodeID = len(keys)-1
        graph["lastNodeID"] = lastNodeID
        linkpairs = []

        for i in range(len(keys)):
            key = keys[i]
            for j in len(adjlist[key]):
                n0 = int(key)
                n1 = adjlist[key][j]

                pair = {"source": n0, "target": n1}
                if pair not in linkpairs:
                    linkpairs.append(pair)
        graph["links"] = map(jsonify, linkpairs)

    ret = nr.main(inputfile, num_nodes, fault_percent, resilience_type)
    map(adjList2linkPairs, ret)
    return ret

"""
Running website
"""

# running the site
if __name__ == '__main__':
    # run this command with any additional arg to run in production
    if len(sys.argv) > 1:
        print('<< PROD >>')
        os.system(f"gunicorn -b '0.0.0.0:{config['port']}' server:app")
    # or just run without an additional arg to run in debug
    else:
        print('<< DEBUG >>')
        app.run(host="0.0.0.0", debug=True)
