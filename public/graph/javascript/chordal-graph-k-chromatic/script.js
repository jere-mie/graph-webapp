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
            if(cnodesIDs != newNodesIDs) {
                nodes = d.nodes
            }
            lastNodeId = d.lastNodeId
            links = d.links
            restart();
        });
}

// get a graph from the server given some user defined parameters
function getGraph(numNodes, numEdges, btnId, deletionStart) {
    d3.json("/api/v1/graph?numNodes="+numNodes+"&numEdges="+numEdges+"&btnId="+btnId+"&deletionStart="+deletionStart)
        .then(function(d) {
            // console.log(nodes)
            // console.log(d.nodes)
            // console.log(links)
            // console.log(lastNodeId)

            // check for error
            if("Error" in d) {
                console.log(d["Error"])
                return
            }

            // update graph
            nodes = d.nodes;
            lastNodeId = d.lastNodeId;
            links = d.links;
            restart()
        });
}

let deletionStart = false; // used for python algorithm

// called button on page
function btnOnClick(btnId) {
    if(btnId == "btnStep2") {
        let miNodes = [];
        nodes.forEach((v) => {
            if(!linkNodes.has(v)) {
                miNodes.push(v)
            }
        });
        miNodes.forEach((mi) => {
            linkNodes.forEach((v) => {
                links.push({source: mi, target:v})
            });
        });

        shouldCheckGraph = false;
        restart();
        document.getElementById("btnStep2").setAttribute("disabled", "");
        document.getElementById("btnStep3").removeAttribute("disabled");

    }
    if(btnId == "btnStep3") {
        let linkNodesList = Array.from(linkNodes);
        
        for(let i=0; i < linkNodesList.length; i++) {
            for(let j=0; j < linkNodesList.length; j++) {
                if(i == j) {continue}
                let newLink = {source: linkNodesList[i], target: linkNodesList[j]}
                add = true

                for(let k=0; k < links.length; k++) {
                    if(links[k].source.id == j && links[k].target.id == i) {
                        add = false
                        break;
                    }
                    if(links[k].source.id == i && links[k].target.id == j) {
                        add = false
                        break;
                    }
                }
                
                if(add) {
                    links.push(newLink);
                }
            }
        }

        restart();
        document.getElementById("btnStep3").setAttribute("disabled", "");
    }
}