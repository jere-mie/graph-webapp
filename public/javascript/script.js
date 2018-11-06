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

// called button on page
function btnOnClick(btnID) {
    if(btnID == "btnCompleteGraph")
        console.log(btnID)

    if(btnID == "btnTree")
        importData("/N4E4/tree.json")

    if(btnID == "btnWCliqueTree")
        console.log(btnID)

    if(btnID == "btnCliqueTree")
        importData("/N4E4/cliqueTree.json")

    if(btnID == "btnChordalGraph")
        importData("/N4E4/chordalGraph.json")
}

