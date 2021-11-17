let nodes = []
let lastNodeId = 0
let links = []

// set up SVG for D3
const width = document.getElementById("svgViewPort").offsetWidth;
const height = document.getElementById("svgViewPort").offsetHeight;
const colors = d3.scaleOrdinal(d3.schemeCategory10);

// select DOM object to display graph
const svg = d3.select('#svgViewPort')
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .on('contextmenu', addNode);

// set file to load on start up
fileName = "N4E4/chordalGraph.json"
importData(fileName);

// radius of nodes
const radius = 10;

// simulation of the graph
const simulation = d3.forceSimulation(nodes)
    .force('charge', d3.forceManyBody().strength(-1000))
    .force('link', d3.forceLink().id((d) => d.id).distance(75))
    .force('x', d3.forceX(width/2))
    .force('y', d3.forceY(height/2))
    .on('tick', () => {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);
        node
            // keep nodes within the viewport since zooming/panning of viewport
            .attr('cx', d => {return d.x = Math.max(radius, Math.min(width - radius, d.x));})
            .attr('cy', d => {return d.y = Math.max(radius, Math.min(height - radius, d.y)); });
    });

// allowing dragging of nodes
const drag = d3.drag()
    .on('start', (d) => {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    })
    .on('drag', (d) => {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    })
    .on('end', (d) => {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    });

let g = svg.append('g').attr('class', 'everything');
let dragLine = g.append('path')
    .attr('class', 'link drageline hidden')
    .attr('d', 'M0,0L0,0');
let link = g.append('g').selectAll('line')
    // .transition().duration(1500).style('stroke', '#999');
let node = g.append('g'). selectAll('circle');

// function to restart the graph
function restart() {
    node = node.data(nodes, d => d.id);
    node.exit().remove();
    const g = node.enter().append('g')
    node = g.append('circle')
        .attr('r', radius)
        .style('fill', d => colors(d.id))
        .style('stroke', d => d3.rgb(colors(d.id)).darker().toString())
        .on('contextmenu', removeNode)
        .on('mousedown', beginDragLine)
        .on('mouseup', endDragLine)
        .merge(node);
    
    // title(mouse hover over)
    node.append('title').text((d) => d.id)
    
    link = link.data(links);
    link.exit().remove();
    link = link.enter()
        .append('line')
        .attr('class', 'link')
        .style('stroke', 'red')
        .style('stroke-width', '4px')
        .on('contextmenu', removeEdge)
        .merge(link);
    
    link.transition()
        .duration(3000)
        .style('stroke', '#333');
    
    simulation.nodes(nodes);
    simulation.force("link").links(links);
    simulation.alphaTarget(0.3).restart();

    checkGraph();

    // drag(node);
}

// nodes that has a link
let linkNodes = new Set();
let shouldCheckGraph = true;

function checkGraph() {
    if(!shouldCheckGraph) {
        return;
    }

    // check if graph is empty
    if(nodes.length < 1) {
        d3.select('#errorSpan').text("Graph can't be empty");
        //document.getElementById("btnStep2").setAttribute("disabled", "");
        return;
    }

    // check if only one conncted component
    componentCount = 1;
    nodes.forEach((v) => {
        v.visted = false;
    });

    // adjacency list
    let adjList = {};
    nodes.forEach((v) => {
        adjList[v.id] = []
    });
    links.forEach((l) => {
        adjList[l.source.id].push(l.target);
        adjList[l.target.id].push(l.source);
    });

    linkNodes.clear();
    links.forEach((l) => {
        linkNodes.add(l.source)
        linkNodes.add(l.target)
    });

    // queue of nodes to vist
    let q = []
    q.push(nodes[0]);

    while(q.length > 0) {
        let v1 = q.shift();
        let adj = adjList[v1.id];

        for(let i=0; i < adj.length; i++) {
            let v2 = adj[i];
            if(v2.visted)
                continue;
            q.push(v2);
        }

        v1.visted = true;
        // if nothing in queue then check if we
        // visted all nodes that are linked
        if(q.length == 0) {
            for(let i=0; i<nodes.length; i++) {
                if(!nodes[i].visted && linkNodes.has(nodes[i])) {
                    q.push(nodes[i]);
                    componentCount++;
                    break;
                }
            }
        }
    }

    if(componentCount > 1) {
        d3.select("#errorSpan").text("Only one connected component")
        //document.getElementById("btnStep2").setAttribute("disabled", "");
        return;
    }

    if(nodes.length - linkNodes.size < 1) {
        d3.select("#errorSpan").text("More than one mutually independent vertex")
        //document.getElementById("btnStep2").setAttribute("disabled", "");
        return;
    }

    d3.select("#errorSpan").text(" ")
    //document.getElementById("btnStep2").removeAttribute("disabled");
}

let mousedownNode = null, mouseupNode = null;

function resetMouseVar() {
    mousedownNode = null;
    mouseupNode = null;
}

function addNode() {
    d3.event.preventDefault();
    d3.event.stopPropagation();
    // if (mousedownNode) return;
    const point = d3.mouse(this);
    const newNode = {id: ++lastNodeId, x: point[0], y: point[1]}
    nodes.push(newNode);
    restart();
}

function addNodeAtPos(posx, posy) {
    //d3.event.preventDefault();
    //d3.event.stopPropagation();
    const newNode = {id: ++lastNodeId, x: posx, y: posy}
    nodes.push(newNode);
    restart();
}

function removeNode(d) {
    nodes.splice(nodes.indexOf(d), 1);
    let linksToRemove = links.filter( (l) => {
        return l.source===d || l.target===d;
    });
    linksToRemove.map( (l) => {
        links.splice(links.indexOf(l),1)
    });
    d3.event.preventDefault();
    d3.event.stopPropagation();
    restart();
}

function removeEdge(d) {
    links.splice(links.indexOf(d), 1);
    d3.event.preventDefault();
    d3.event.stopPropagation();
    restart();
}

function beginDragLine(d) {
    simulation.stop();
    mousedownNode = d;

    dragLine
        .classed('hidden', false)
        .attr('d', `M${mousedownNode.x},${mousedownNode.y}L${mousedownNode.x},${mousedownNode.y}`);
    
    d3.event.stopPropagation();
    restart();
    simulation.stop();
}

function updateDragLine() {
    if(!mousedownNode) return;
    // update drag line
    dragLine.attr('d', `M${mousedownNode.x},${mousedownNode.y}L${d3.mouse(this)[0]},${d3.mouse(this)[1]}`);
    restart();
    simulation.stop();
}

function hideDragLine() {
    dragLine.classed('hidden', true);
    resetMouseVar();
    restart();
}

function endDragLine(d) {
    // if mouse does not release on node or self reference then skip
    if(!mousedownNode || mousedownNode===d) {
        resetMouseVar();
        return;
    }

    // check if link already exists
    for(let i =0; i < links.length; i++) {
        let l = links[i];
        if((l.source===mousedownNode && l.target===d) || (l.source===d && l.target===mousedownNode)) {
            console.log("link already exits")
            return;
        }
    }

    // add the link
    let newLink = {source: mousedownNode, target: d};
    links.push(newLink);

    restart();
}

svg.on('mousemove', updateDragLine)
    .on('mouseup', hideDragLine)
    .on('mouseleave', hideDragLine)
restart();
