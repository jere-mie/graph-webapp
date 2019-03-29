const express = require('express')
const ps = require('python-shell')
const app = express()

app.use(express.static('public/graph')) // graph page files
app.use(express.static('public/main'))  // main page files

// get port number from enviromne
// process.env.PORT
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

app.get('/api/v1/graph', (req, res) => {
    let numNodes = req.query.numNodes
    let numEdges = req.query.numEdges
    let btnId = req.query.btnId
    let deletionStart = req.query.deletionStart

    if(isNaN(numNodes) || isNaN(numEdges)) {
        return res.status(200).send()
    }

    // python program does not create complete graph
    if (btnId == 'btnCompleteGraph') {
        graph = {}
        graph["nodes"] = []
        for (i=0; i < numNodes; i++) {
            graph["nodes"].push({id:i})
        }
        graph["lastNodeId"] = numNodes - 1
        graph["links"] = []
        for (i=0; i < numNodes; i++) {
            for (j=i; j < numNodes; j++) {
                if (i != j) {
                    graph["links"].push({"source":i, "target":j})
                }
            }
        }
        
        return res.status(200).send(graph)
    }

    console.log("Python Started with numNodes:" + numNodes + " numeEdges:" + numEdges + " btnId:" + btnId)
    runPythonScript('Py_Program/','interface.py', [numNodes, numEdges, btnId, deletionStart], callback)

    function callback(output) {
        keys = Object.keys(output)
        graph = {}
        nodes = keys.map(x => ({id:x}))
        graph["nodes"] = nodes
        lastNodeId = keys.length
        graph["lastNodeId"] = lastNodeId

        linkpairs = []

        function createLink(source, target) {
            return JSON.stringify({"source": source, "target": target})
        }
        
        for(i=0; i < keys.length; i++) {
            key = keys[i]
            // for(node in output[key]) {
            for(j=0; j < output[key].length; j++) {
                node0 = parseInt(key)
                node1 = output[key][j]
                if(linkpairs.includes(createLink(node1, node0))) {
                    continue
                } else {
                    linkpairs.push(createLink(node0,node1))
                }
            }
        }

        graph["links"]= linkpairs.map(JSON.parse)
        console.log("Python done")
        
        return res.status(200).send(graph)
    }

})