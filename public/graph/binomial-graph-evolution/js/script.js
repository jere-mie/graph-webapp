function importData(fileName) {
    d3.json("../data/".concat(fileName))
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
        updateLabels();
}

// called button on page
function btnOnClick(btnId) {
    if(btnId == "btnGenGraph") {
        edges = [];
    	rvalues = [];

        numNodes = parseInt(document.getElementById('numNodes').value);

        //console.log(nodes)
        

        nodes = [];
        links = [];
        //console.log(nodes)
        //addNodeAtPos(15,15);
        for(j=0; j<numNodes; j++){
            //addNodeAtPos(10+i*5,15);
            addNodeAtPos(0,0);
        }
        console.log(nodes);
        //step 1: create lexographic ranking of the index pairs
        //const combinations = k_combinations(nodes, 2)

        //THIS IS WHERE WE LOAD THE COMBINATION ARRAY
       	combinations = comb(nodes);
       	//THIS IS WHERE WE PRINT THE COMBINATION ARRAY AND IT IS NOT IN ORDER
       	console.log(combinations);

       	//combinations.sort();
       	//combinations = array.sort(function(a, b) {
  		//if (a[0] == b[0]) {
    	//	return a[1] - b[1];
  		//}
  		//return b[0] - a[0];
		//});

       	console.log(combinations)
        //step 2: set k=0, i=0
        i=0;
        k=0;

        while(combinations.length-k > 0){ //step 6: If combinations.length-k > 0 go to Step 3.
            //step 3: generate r
            x = Math.random();
            r = 1 + Math.round(x*((combinations.length-1-k)-1));
            console.log(combinations)
            if(combinations[r] == undefined){
            	r += 1;
            }
            //step 4: join vertices

             if(combinations[r] == undefined){
                //combinations.splice(r,r+1);
                continue;
            }
            
            let newLink = {source: combinations[r][0], target: combinations[r][1]}
            edges.push(newLink);
            rvalues.push(r);
            i = i+1;

            //step 5: swap
            temp = combinations[r];
            combinations[r] = combinations[combinations.length-k];
            combinations[combinations.length-k] = temp;
            k = k+1;
            restart();
        }

        document.getElementById('nodeLabel').value = "Nodes: "+nodes.length;
        document.getElementById('edgeLabel').value = "Edges: "+edges.length;
        document.getElementById("btnNext").disabled = false;
    }
    if(btnId == "btnNext"){
    	console.log(rvalues)
    	updateLabels();
    	document.getElementById('Graph info').value += "generated Index: "+rvalues.shift().toString()+"\n";
    	pass = 1;
        if(edges.length != 0){
        	edge = edges.shift();
        	if(links.includes(edge)){
        	}
        	for(i=0; i<links.length; i++){
        		if(edge.target.id == links[i].target.id && edge.source.id == links[i].source.id){
    				//document.getElementById('Graph info').value += "This Edge has already been added\n";
    				pass = 0;
        		}
        	}
        	if(pass == 1){
        		links.push(edge);
            	console.log(edge);
        	}
            restart();
        }
        updateLabels();
        //console.log(edges)
        if(edges.length == 0){
        	document.getElementById("btnNext").disabled = true;
        	document.getElementById('Graph info').value += "Max number of Edges were added\n";		
        }
    }
    
}

function updateLabels() {
	document.getElementById('nodeLabel').innerHTML = "Nodes: "+nodes.length;
    document.getElementById('edgeLabel').innerHTML = "Edges: "+links.length;
}

// THIS IS THE COMBINATION FUNCTION WE ARE USING (ONE THAT IS NOT PUSHING VALUES IN SORTED ORDER)
function comb(set){
	var combs = []
	for (var node = 0; node < set.length; node++) {
		console.log(set[node]);
		for (var otherNode = node + 1; otherNode < set.length; otherNode++) {
			var pair = [set[node], set[otherNode]]
			console.log("others")
			//console.log(set[otherNode])
			console.log(pair);
				//if(!combs.includes(pair)){
			combs.push(pair);
				//}
		}
	}
	//console.log(combs)
	return combs;
}