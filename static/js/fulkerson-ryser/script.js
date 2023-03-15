// global var for fulkerson api output
var fulkersonOutput = "";
var fulkersonIndex = 0;

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

function fulkersonGenerate(){
    document.getElementById('genBtn').setAttribute('disabled', 'true');
    let indeglist = document.getElementById("indeglist");
    let outdeglist = document.getElementById("outdeglist");
    let numNodes = indeglist.value.split(',').length;
    console.log(numNodes);
    const url = "/api/fulkerson?indegrees=" + encodeURIComponent(indeglist.value) + "&outdegrees=" + encodeURIComponent(outdeglist.value);
    fetch(url)
    .then(response => response.json())
    .then(data => {
        fulkersonOutput = data;
        console.log(data);
        nodes = [];
        links = [];
        for(let i=0; i<numNodes; i++){
            nodes.push({id:i});
            restart();
        }
        fulkersonNext();
    })
    .catch(error => console.error(error));
}

function fulkersonNext(){
    if(fulkersonOutput.length <= fulkersonIndex){
        alert("Cannot go further!");
        return;
    }
    let currOutput = fulkersonOutput[fulkersonIndex];
    alert(`Case ${currOutput['case']} found!`);

    for(let i=0; i<currOutput.addEdge.length; i++){
        let currEdge = currOutput.addEdge[i];
        links.push({
            source:nodes[getNodeIdxById(currEdge[0]-1)],
            target:nodes[getNodeIdxById(currEdge[1]-1)],            
        });
        restart();
    }

    for(let i=0; i<currOutput.delEdge.length; i++){
        let currEdge = currOutput.delEdge[i];
        // find the edge we need to remove and remove it
        for(let j=0; j<links.length; j++){
            if(links[j].source.id == currEdge[0]-1 && links[j].target.id == currEdge[1]-1){
                links.slice(j, 1);
                restart();
                break;
            }
        }
    }

    fulkersonIndex++;
    if(fulkersonOutput.length <= fulkersonIndex){
        document.getElementById('nextBtn').setAttribute('disabled', 'true');
        return;
    }
}

function fulkersonRandomize(){
    alert("not yet implemented");
}