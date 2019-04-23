const express = require('express')
const ps = require('python-shell')
const app = express()

app.use(express.static('public/graph')) // graph page files
app.use(express.static('public/main'))  // main page files

// get port number from enviroment
// const port = process.env.PORT
const port = 3000

app.listen(port, () => console.log(`app running at http://localhost:${port}`))

function runPythonScript(scriptPath, scriptName, args, callback) {
    let output = ''
    let py_options = {}
    
    if(process.platform === "win32") {
        py_options = {
            mode: 'text',
            pythonPath: 'C:/Python27/python.exe',
            pythonOptions: [], // get print results in real-time
            scriptPath: scriptPath,
            args: args
        };
    } else {
        py_options = {
            mode: 'text',
            pythonPath: '/usr/bin/python',
            pythonOptions: [], // get print results in real-time
            scriptPath: scriptPath,
            args: args
        };
    }

    ps.PythonShell.run(scriptName, py_options, (err, results) => {
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        output = results[results.length-1]
        // console.log('results: %j', results[results.length-1])
        callback(JSON.parse(output))
    });
}

app.get('/api/v1/unified-graph', (req, res) => {
    let numNodes = req.query.numNodes
    let numEdges = req.query.numEdges
    let deletionStart = req.query.deletionStart

    errors = []
    // return res.status(400).send({"Error": "Invalid "})
    // check input
    if(isNaN(numNodes)) { errors.push("numNodes is NaN") }
    if(isNaN(numEdges)) { errors.push("numEdges is NaN") }
    if(numEdges < 1) { errors.push("numedges < 1") }
    if(numNodes < 1) { errors.push("numNodes < 1") }

    // return error
    if(errors.length != 0) {
        return res.status(200).send({"Error": errors})
    }

    // python program does not create complete graph
    if (deletionStart == 'true' && parseInt(numNodes) <= 50) {
        completeGraph = {}
        completeGraph["nodes"] = []
        for (i=0; i < numNodes; i++) {
            completeGraph["nodes"].push({id:i})
        }
        completeGraph["lastNodeId"] = numNodes - 1
        completeGraph["links"] = []
        for (i=0; i < numNodes; i++) {
            for (j=i; j < numNodes; j++) {
                if (i != j) {
                    completeGraph["links"].push({"source":i, "target":j})
                }
            }
        }
    }

    console.log("Python Started with numNodes:" + numNodes + " numeEdges:" + numEdges + " deletionStart:" + deletionStart)
    runPythonScript('Py_Program/','chordal-graph-Unified-Interface.py', [numNodes, numEdges, deletionStart], callback)

    function callback(output) {
        function adjList2linkPairs(adjList) {
            let keys = Object.keys(adjList)
            let graph = {}
            let nodes = keys.map(x => ({id:x}))
            graph["nodes"] = nodes
            let lastNodeId = keys.length - 1
            graph["lastNodeId"] = lastNodeId

            let linkpairs = []

            function createLink(source, target) {
                return JSON.stringify({"source": source, "target": target})
            }
            
            // loop throught adjacency list 
            for(i=0; i < keys.length; i++) {
                key = keys[i]
                // loop through list of connected nodes
                for(j=0; j < adjList[key].length; j++) {
                    node0 = parseInt(key)
                    node1 = adjList[key][j]
                    // check if link already exists
                    if(linkpairs.includes(createLink(node1, node0))) {
                        continue
                    } else {
                        linkpairs.push(createLink(node0,node1))
                    }
                }
            }

            graph["links"] = linkpairs.map(JSON.parse)
            return graph
        }

        console.log("Python done")
        graphs = output.map(adjList2linkPairs)
        if(deletionStart  == 'true' && parseInt(numNodes) <= 50) {
            graphs[0] = completeGraph
        }
        return res.status(200).send(graphs)
    }

})