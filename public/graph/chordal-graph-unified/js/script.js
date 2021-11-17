function importData(fileName) {
    d3.json("../data/".concat(fileName))
        .then(function(d) {
            // console.log(nodes)
            // console.log(d.nodes)
            // console.log(links)
            // console.log(lastNodeId)

            // check if nodes have changed
            const cnodesIDs = nodes.map(n => n.id).toString();
            const newNodesIDs = d.nodes.map(n => n.id).toString();
            if(cnodesIDs != newNodesIDs) {
                nodes = d.nodes;
            }
            lastNodeId = d.lastNodeId;
            links = d.links;
            restart();
        });
}

function getGraph(numNodes, numEdges, deletionStart, callback) {
    d3.json("/api/unified-graph?numNodes="+numNodes+"&numEdges="+numEdges+"&deletionStart="+deletionStart)
        .then(function(d) {
            // console.log(nodes)
            // console.log(d.nodes)
            // console.log(links)
            // console.log(lastNodeId)

            // check for error
            if("Error" in d) {
                return console.warn(d["Error"]);
            }

            callback(d);
        });
}

let deletionStart = false; // used for algorithm
let graphs; // holds the graphs for each step

// called button on page
function btnOnClick(btnId) {
    if(btnId == "btnCompleteGraph" || btnId == "btnTree") {
        // get input
        numNodes = parseInt(document.getElementById('numNodes').value);
        numEdges = parseInt(document.getElementById('numEdges').value);

        if(btnId == "btnCompleteGraph") {
            deletionStart = true;
        } else if (btnId == "btnTree") {
            deletionStart = false;
        }

        // No complete graphs where number of nodes > 50
        if(btnId == "btnCompleteGraph" && numNodes > 50) {
            document.getElementById("Alert").removeAttribute("hidden");
            setTimeout(() => {document.getElementById("Alert").setAttribute("hidden","")}, 10000);
        }

        function updateGraph(gs) {
            graphs = gs;
            console.log(graphs);
            // update the graph
            nodes = graphs[0].nodes;
            lastNodeId = graphs[0].lastNodeId;
            links = graphs[0].links;
            restart();
        }

        getGraph(numNodes, numEdges, deletionStart, updateGraph);        

        // disable the input
        document.getElementById('numNodes').disabled = true;
        document.getElementById('numEdges').disabled = true;

        // disable step 1
        document.getElementById("btnCompleteGraph").setAttribute("disabled", "");
        document.getElementById("btnTree").setAttribute("disabled", "");

        // enable step 2
        document.getElementById("btnCliqueTree").removeAttribute("disabled");
    } else if (btnId == "btnCliqueTree") {
        // update the graph for step 2
        nodes = graphs[1].nodes;
        lastNodeId = graphs[1].lastNodeId;
        links = graphs[1].links;
        restart();

        // disable step 2
        document.getElementById("btnCliqueTree").setAttribute("disabled", "");
        // enable step 3
        document.getElementById("btnChordalGraph").removeAttribute("disabled");
    } else if (btnId == "btnChordalGraph") {
        // update the graph for step 3
        nodes = graphs[2].nodes;
        lastNodeId = graphs[2].lastNodeId;
        links = graphs[2].links;
        restart();

        // disable step 3
        document.getElementById("btnChordalGraph").setAttribute("disabled", "");
    }
}