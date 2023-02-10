function importData(fileName) {
    d3.json("/static/data/".concat(fileName))
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

// called button on page
function btnOnClick(btnId) {
    if(btnId == "btnGenGraph") {
        edges = [];
        
        numNodes = parseInt(document.getElementById('numNodes').value);
        prob = parseFloat(document.getElementById('prob').value);

        //console.log(nodes)
        

        nodes = [];
        links = [];
        console.log(nodes)
        //addNodeAtPos(15,15);
        for(i=0; i<numNodes; i++){
            //addNodeAtPos(10+i*5,15);
            addNodeAtPos(0,0);
        }
        const combinations = k_combinations(nodes, 2)
        console.log(combinations)
        for(i=0; i<combinations.length; i++){
           x = Math.random();
           if(x < prob){
                //setTimeout(() => {
                  let newLink = {source: combinations[i][0], target: combinations[i][1]}
                  edges.push(newLink);
                  restart();
                //}, 1000);
           }
        }   
        //console.log(nodes)
    }


    if(btnId == "btnNext"){
        if(edges.length != 0){
            links.push(edges.shift());
            restart();
        }
        //console.log(edges)
    }
    
}
function k_combinations(set, k) {
    var i, j, combs, head, tailcombs;
    
    // There is no way to take e.g. sets of 5 elements from
    // a set of 4.
    if (k > set.length || k <= 0) {
        return [];
    }
    
    // K-sized set has only one K-sized subset.
    if (k == set.length) {
        return [set];
    }
    
    // There is N 1-sized subsets in a N-sized set.
    if (k == 1) {
        combs = [];
        for (i = 0; i < set.length; i++) {
            combs.push([set[i]]);
        }
        return combs;
    }
    
    // Assert {1 < k < set.length}
    
    // Algorithm description:
    // To get k-combinations of a set, we want to join each element
    // with all (k-1)-combinations of the other elements. The set of
    // these k-sized sets would be the desired result. However, as we
    // represent sets with lists, we need to take duplicates into
    // account. To avoid producing duplicates and also unnecessary
    // computing, we use the following approach: each element i
    // divides the list into three: the preceding elements, the
    // current element i, and the subsequent elements. For the first
    // element, the list of preceding elements is empty. For element i,
    // we compute the (k-1)-computations of the subsequent elements,
    // join each with the element i, and store the joined to the set of
    // computed k-combinations. We do not need to take the preceding
    // elements into account, because they have already been the i:th
    // element so they are already computed and stored. When the length
    // of the subsequent list drops below (k-1), we cannot find any
    // (k-1)-combs, hence the upper limit for the iteration:
    combs = [];
    for (i = 0; i < set.length - k + 1; i++) {
        // head is a list that includes only our current element.
        head = set.slice(i, i + 1);
        // We take smaller combinations from the subsequent elements
        tailcombs = k_combinations(set.slice(i + 1), k - 1);
        // For each (k-1)-combination we join it with the current
        // and store it to the set of k-combinations.
        for (j = 0; j < tailcombs.length; j++) {
            combs.push(head.concat(tailcombs[j]));
        }
    }
    return combs;
}