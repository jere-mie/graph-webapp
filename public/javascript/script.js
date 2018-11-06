// used by app.js
nodes = []
lastNodeId = 0
links = []

// import json data from file and set node, lastNodeId and links variables
function importData(fileName) {
    d3.json(fileName)
        .then(function(d) {
            console.log(d);
            nodes = d.nodes
            lastNodeId = d.lastNodeId
            links = d.links
            restart()
        });
}
