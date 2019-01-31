const express = require('express')
const ps = require('python-shell')
const app = express()

app.use(express.static('public/graph')) // graph page files
app.use(express.static('public/main'))  // main page files

// get port number from enviromne
// process.env.PORT
const port = 3000

app.listen(port, () => console.log(`app running at http://localhost:${port}`))

app.get('/api/v1/graph', (req, res) => {
    let numNodes = req.query.numNodes
    let numEdges = req.query.numEdges
    let btnId = req.query.btnId
    let deletionStart = req.query.deletionStart

    if(isNaN(numNodes) || isNaN(numEdges)) {
        return res.status(200).send()
    }

    let output = ''
    let py_options = {}
    
    if(process.platform === "win32") {
        py_options = {
            mode: 'text',
            pythonPath: 'C:/Python27/python.exe',
            pythonOptions: [], // get print results in real-time
            scriptPath: 'Py_Program/',
            args: [numNodes, numEdges, btnId, deletionStart]
        };
    } else {
        py_options = {
            mode: 'text',
            pythonPath: '/usr/bin/python',
            pythonOptions: [], // get print results in real-time
            scriptPath: 'Py_Program/',
            args: [numNodes, numEdges, btnId, deletionStart]
        };
    }

    ps.PythonShell.run('interface.py', py_options, (err, results) => {
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        output = results[results.length-1]
        // console.log('results: %j', results[results.length-1])
        test1(JSON.parse(output))
    });

    function test1(output) {
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

        return res.status(200).send(graph)
    }

})