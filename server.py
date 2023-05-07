import os
import json
import sys
from flask import Flask, abort, jsonify, render_template, request
from graph_algos.chordal_graph_interface import generateCG
from graph_algos import FR_DirectedGraphGeneration as kw
from graph_algos import NetworkResilience as nr
from graph_algos import HavelHakimi as hh
import networkx as nx

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
    if name not in {"chordal-graph-k-chromatic", "unified-chordal-graph", "random-graph-evolution", "binomial-graph-evolution", "network-resilience-test", 'fulkerson-ryser', 'havel-hakimi'}:
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

@app.route('/api/network_resilience', methods=['GET'])
def network_resilience():
    inputfile = request.args.get("file")
    num_nodes = request.args.get("num_nodes")
    fault_percent = request.args.get("fault_percent");
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
