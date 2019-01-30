nodes = []
lastNodeId = 0
links = []

function importData(fileName) {
    d3.json("data/".concat(fileName))
        .then(function(d) {
            // console.log(nodes)
            // console.log(d.nodes)
            // console.log(links)
            // console.log(lastNodeId)

            // check if nodes have changed
            const cnodesIDs = nodes.map(n => n.id).toString()
            const newNodesIDs = d.nodes.map(n => n.id).toString()
            if(cnodesIDs != newNodesIDs)
                nodes = d.nodes
            lastNodeId = d.lastNodeId
            links = d.links
            restart()
        });
}

function getGraph(numNodes, numEdges, btnId, deletionStart) {
    d3.json("/api/v1/graph?numNodes="+numNodes+"&numEdges="+numEdges+"&btnId="+btnId+"&deletionStart="+deletionStart)
        .then(function(d) {
            // console.log(nodes)
            // console.log(d.nodes)
            // console.log(links)
            // console.log(lastNodeId)

            // check if nodes have changed
            const cnodesIDs = nodes.map(n => n.id).toString()
            const newNodesIDs = d.nodes.map(n => n.id).toString()
            if(cnodesIDs != newNodesIDs)
                nodes = d.nodes
            lastNodeId = d.lastNodeId
            links = d.links
            restart()
        });
}

let deletionStart = false; // used for algorithm

// called button on page
function btnOnClick(btnId) {
    if(btnId == "btnCompleteGraph") {
        // get input
        numNodes = parseInt(document.getElementById('numNodes').value)
        numEdges = parseInt(document.getElementById('numEdges').value)

        deletionStart = true
        getGraph(numNodes, numEdges, btnId, deletionStart)


        // disable step 1
        document.getElementById("btnCompleteGraph").setAttribute("disabled", "");
        document.getElementById("btnTree").setAttribute("disabled", "");
        // enable step 2
        document.getElementById("btnCliqueTree").removeAttribute("disabled");
        console.log(btnId)
    }
    if(btnId == "btnTree") {
        // get input
        numNodes = parseInt(document.getElementById('numNodes').value)
        numEdges = parseInt(document.getElementById('numEdges').value)

        deletionStart = false
        getGraph(numNodes, numEdges, btnId, deletionStart)

        // disable step 1
        document.getElementById("btnCompleteGraph").setAttribute("disabled", "");
        document.getElementById("btnTree").setAttribute("disabled", "");
        // enable step 2
        document.getElementById("btnCliqueTree").removeAttribute("disabled");

    }

    if(btnId == "btnWCliqueTree")
        console.log(btnId)

    if(btnId == "btnCliqueTree") {
        // get input
        numNodes = parseInt(document.getElementById('numNodes').value)
        numEdges = parseInt(document.getElementById('numEdges').value)

        getGraph(numNodes, numEdges, btnId, deletionStart)

        // disable step 2
        document.getElementById("btnCliqueTree").setAttribute("disabled", "");
        // enable step 3
        document.getElementById("btnChordalGraph").removeAttribute("disabled");
    }

    if(btnId == "btnChordalGraph") {
        // importData("/N4E4/chordalGraph.json")
        // get input
        numNodes = parseInt(document.getElementById('numNodes').value)
        numEdges = parseInt(document.getElementById('numEdges').value)

        getGraph(numNodes, numEdges, btnId, deletionStart)
    }
}

