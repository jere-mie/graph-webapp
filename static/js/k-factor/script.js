function importData(fileName) {
    d3.json("/static/data/".concat(fileName))
        .then(function(d) {

            // check if nodes have changed
            // Original graph
            const cnodesIDs = nodes.map(n => n.id).toString()
            const newNodesIDs = d.nodes.map(n => n.id).toString()
            if(cnodesIDs != newNodesIDs) {
                nodes = d.nodes
            }
            lastNodeId = d.lastNodeId
            links = d.links
            restart();

            // K-factor graph
            const cnodesIDs2 = nodes2.map(n => n.id).toString()
            const newNodesIDs2 = d.nodes2.map(n => n.id).toString()
            if(cnodesIDs2 != newNodesIDs2) {
                nodes2 = d.nodes2
            }
            lastNodeId2 = d.lastNodeId2
            links2 = d.links2
            restart();

            // d - k graph
            const cnodesIDs3 = nodes3.map(n => n.id).toString()
            const newNodesIDs3 = d.nodes3.map(n => n.id).toString()
            if(cnodesIDs3 != newNodesIDs3) {
                nodes3 = d.nodes3
            }
            lastNodeId3 = d.lastNodeId3
            links3 = d.links3
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

function kfactor(){
    let deglist = document.getElementById("deglist");
    let k_val = document.getElementById("k_val");
    const url = "/api/k-factor?degreelist=" + encodeURIComponent(deglist.value) + encodeURIComponent(',' + k_val.value);
    console.log(url);
    fetch(url)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        nodes = [];
        links = [];
        let numNodes = data[0]['nodeList'].length;
        for(let i=0; i<numNodes; i++){
            nodes.push({id:i});
            restart();
        }
        let outEdges = data[0]['edgeList'];
        for(let edge of outEdges){
            links.push({
                source:nodes[edge[0]],
                target:nodes[edge[1]]
            })
        }

        restart();
        nodes2 = [];
        links2 = [];
        let numNodes2 = data[1]['nodeList'].length;
        for(let i=0; i<numNodes2; i++){
            nodes2.push({id:i});
            restart();
        }
        let outEdges2 = data[1]['edgeList'];
        for(let edge of outEdges2){
            links2.push({
                source:nodes2[edge[0]],
                target:nodes2[edge[1]]
            })
        }
        restart();

        nodes3 = [];
        links3 = [];
        let numNodes3 = data[2]['nodeList'].length;
        for(let i=0; i<numNodes3; i++){
            nodes3.push({id:i});
            restart();
        }
        let outEdges3 = data[2]['edgeList'];
        for(let edge of outEdges3){
            links3.push({
                source:nodes3[edge[0]],
                target:nodes3[edge[1]]
            })
        }
        restart();
    })
    .catch(error => console.error(error));
}

function giveConnected(){
    const url = "/api/give_sequence?type=connected"
    console.log(url)
    fetch(url)
    .then(response => response.json())
    .then(data => {
        k = data.pop()
        console.log(data);
        console.log("K: " + k)
        // Edit form to have generated sequence
        sequence_form = document.getElementById("deglist");
        k_form = document.getElementById("k_val");
        sequence_form.value = data;
        k_form.value = k
    }
    )
    .catch(error => console.error(error));
}

function giveDisconnected(){
    const url = "/api/give_sequence?type=disconnected"
    console.log(url)
    fetch(url)
    .then(response => response.json())
    .then(data => {
        k = data.pop()
        console.log(data);
        console.log("K: " + k)
        // Edit form to have generated sequence
        sequence_form = document.getElementById("deglist");
        k_form = document.getElementById("k_val");
        sequence_form.value = data;
        k_form.value = k
    }
    )
    .catch(error => console.error(error));
}