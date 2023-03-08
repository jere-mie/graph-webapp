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

function fulkersonGenerate(){
    let indeglist = document.getElementById("indeglist");
    let outdeglist = document.getElementById("outdeglist");
    
    const url = "/api/fulkerson?indegrees=" + encodeURIComponent(indeglist.value) + "&outdegrees=" + encodeURIComponent(outdeglist.value);
    fetch(url)
    .then(response => response.json())
    .then(data => fulkersonOutput = data)
    .catch(error => console.error(error));
}

function fulkersonNext(){
    // this doesn't do what we actually want it to yet
    let source = parseInt(window.prompt("source id"));
    let target = parseInt(window.prompt("target id"));
    links.push({source:nodes[source], target:nodes[target]});
    restart();
}

function fulkersonRandomize(){
    alert("not yet implemented");
}