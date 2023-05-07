function importData(fileName) {
    d3.json("/static/data/".concat(fileName))
        .then(function(d) {

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

function getNodeIdxById(id){
    for(let i=0; i<nodes.length; i++){
        if(nodes[i].id == id){
            return i;
        }
    }
    return -1;
}

function havelHakimi(){
    let deglist = document.getElementById("deglist");
    const url = "/api/havelhakimi?degreelist=" + encodeURIComponent(deglist.value);
    fetch(url)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        nodes = [];
        links = [];
        let numNodes = data['nodeList'].length;
        for(let i=0; i<numNodes; i++){
            nodes.push({id:i});
            restart();
        }
        let outEdges = data['edgeList'];
        for(let edge of outEdges){
            links.push({
                source:nodes[edge[0]],
                target:nodes[edge[1]]
            })
        }
        restart();
    })
    .catch(error => console.error(error));
}
