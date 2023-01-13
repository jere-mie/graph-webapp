import os
import json
import sys
from flask import Flask, abort, jsonify, render_template, request
from chordal_graph_interface import generateCG

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
    nodes = request.args.get('nodes')
    edges = request.args.get('edges')
    deletion_start = request.args.get('deletionstart')

    if not nodes:
        abort(400, description="Node(s) not found")
    if not edges:
        abort(400, description="Edge(s) not found")
    if nodes < 1:
        abort(400, description="nodes < 1")
    if edges < 1:
        abort(400, description="edges < 1")

    graphs = generateCG(nodes, edges, deletion_start)
    return jsonify(graphs)

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
