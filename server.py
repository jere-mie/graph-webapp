import os
import json
import sys
from flask import Flask, abort, jsonify, render_template, request
from chordal_graph_interface import generateCG
import FulkersonRyserV2.DirectedGraphGeneration.py

# getting config details
with open('config.json') as f:
    data = json.load(f)

# initializing Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = data['secret_key']

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

# Error handlers
@app.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400

# API endpoints for frontend to consume

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

@app.route('/api/fulkerson', methods=['GET']) # we are receiving two lists from frontent, indegrees and outdegrees
def fulkersonryser():
    indegrees = list(request.args.get("indegrees"))
    outdegrees = list(request.args.get("outdegrees"))
    num_nodes = len(outdegrees)

    degList=[]
    valid = 1

    for i in range(num_nodes):

        v1 = v1 + indeg
        v2 = v2 + outdeg
        if (v1 >= num_nodes or v2 >= num_nodes):
            print ("graph cannot be created")
            valid = 0
        degList.append(degValue) # adding the element
    if (indeg != outdeg):
        valid = 0
    if (valid == 1):
        sortedDegList = kw.sortVertices(degList, n)
        kw.constructDirectedGraph(G, sortedDegList, n)
        kw.displayGraph(G)



@app.route('/graph/<name>', methods=['GET'])
def graphapp(name):
    if name not in {"chordal-graph-k-chromatic", "unified-chordal-graph", "random-graph-evolution", "binomial-graph-evolution", "network-resilience-test"}:
        abort(404)
    return render_template(f'{name}.html')


# running the site
if __name__=='__main__':
    # run this command with any additional arg to run in production
    if len(sys.argv) > 1:
        print('<< PROD >>')
        os.system(f"gunicorn -b '127.0.0.1:{data['port']}' server:app")
    # or just run without an additional arg to run in debug
    else:
        print('<< DEBUG >>')
        app.run(debug=True)
