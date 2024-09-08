let nodes = []
let lastNodeId = 0
let links = []

let nodes2 = []
let lastNodeId2 = 0
let links2 = []

let nodes3 = []
let lastNodeId3 = 0
let links3 = []

// set up SVG for D3
const width = document.getElementById("svgViewPort").offsetWidth;
const height = document.getElementById("svgViewPort").offsetHeight;
const colors = d3.scaleOrdinal(d3.schemeCategory10);

const svg = d3.select('#svgViewPort')
    .append('svg')
    // .attr('oncontextmenu', 'return false;')
    .attr('width', width)
    .attr('height', height);

// this adds arrows to make the graph directed
// svg.append("svg:defs").selectAll("marker")
//     .data(["end"])      // Different link/path types can be defined here
//     .enter().append("svg:marker")    // This section adds in the arrows
//     .attr("id", String)
//     .attr("viewBox", "0 -5 10 10")
//     .attr("refX", 15)
//     .attr("refY", 0.5)
//     .attr("markerWidth", 3)
//     .attr("markerHeight", 5)
//     .attr("orient", "auto")
//     .append("svg:path")
//     .attr("d", "M0,-5L10,0L0,5");

// set file to load on start up
fileName = "N4E4/kfactor.json"
importData(fileName);

const simulation = d3.forceSimulation(nodes)
    .force('charge', d3.forceManyBody().strength(-1000))
    .force('link', d3.forceLink().id((d) => d.id).distance(75))
    .force('x', d3.forceX(width/2))
    .force('y', d3.forceY((height/2) - 300))
    .on('tick', () => {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y)
            // .attr("marker-end", "url(#end)"); // also for adding arrows
        node
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);
    });

const simulation2 = d3.forceSimulation(nodes2)
    .force('charge', d3.forceManyBody().strength(-1000))
    .force('link', d3.forceLink().id((d) => d.id).distance(75))
    .force('x', d3.forceX((width/2) - 200))
    .force('y', d3.forceY(height/2))
    .on('tick', () => {
        link2
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);
            // .attr("marker-end", "url(#end)"); // also for adding arrows
        node2
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);
    });

const simulation3 = d3.forceSimulation(nodes3)
    .force('charge', d3.forceManyBody().strength(-1000))
    .force('link', d3.forceLink().id((d) => d.id).distance(75))
    .force('x', d3.forceX((width/2) + 200))
    .force('y', d3.forceY(height/2))
    .on('tick', () => {
        link3
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);
            // .attr("marker-end", "url(#end)"); // also for adding arrows
        node3
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);
    });

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
let link = g.append('g').selectAll('line');
let node = g.append('g'). selectAll('circle');
let title = g.append('text')
    .attr("x", (width/2))
    .attr("y", (height/2) - 500)
    .attr("text-anchor", "middle")
    .style("font-size", "16px")
    .style("text-decoration", "underline")
    .text("Original Graph");

let g2 = svg.append('g').attr('class', 'everything');
let link2  = g2.append('g').selectAll('line');
let node2 = g2.append('g'). selectAll('circle');
let title2 = g2.append('text')
    .attr("x", (width/2) - 200)
    .attr("y", (height/2) - 200)
    .attr("text-anchor", "middle")
    .style("font-size", "16px")
    .style("text-decoration", "underline")
    .text("k-Factor Graph");

let g3 = svg.append('g').attr('class', 'everything');
let link3  = g3.append('g').selectAll('line');
let node3 = g3.append('g'). selectAll('circle');
let title3 = g3.append('text')
    .attr("x", (width/2) + 200)
    .attr("y", (height/2) - 200)
    .attr("text-anchor", "middle")
    .style("font-size", "16px")
    .style("text-decoration", "underline")
    .text("d-k Graph");

function restart() {
    // Original graph
    node = node.data(nodes, d => d.id);
    node.exit().remove();
    node = node.enter()
        .append('circle')
        .attr('r', 10)
        .style('fill', d => colors(d.id))
        .style('stroke', d => d3.rgb(colors(d.id)).darker().toString())
        .merge(node);
    
    node.append('title').text((d) => d.id)
    
    link = link.data(links);
    link.exit().remove();
    link = link.enter()
        .append('line')
        .attr('class', 'link')
        .style('stroke', '#333')
        .style('stroke-width', '4px')
        .merge(link);
    
    simulation.nodes(nodes);
    simulation.force("link").links(links);
    simulation.alphaTarget(0.3).restart();

    drag(node);

    // k-factor graph
    node2 = node2.data(nodes2, d => d.id);
    node2.exit().remove();
    node2 = node2.enter()
        .append('circle')
        .attr('r', 10)
        .style('fill', d => colors(d.id))
        .style('stroke', d => d3.rgb(colors(d.id)).darker().toString())
        .merge(node2);
    
    node2.append('title').text((d) => d.id)
    
    link2 = link2.data(links2);
    link2.exit().remove();
    link2 = link2.enter()
        .append('line')
        .attr('class', 'link')
        .style('stroke', '#333')
        .style('stroke-width', '4px')
        .merge(link2);
    
    simulation2.nodes(nodes2);
    simulation2.force("link").links(links2);
    simulation2.alphaTarget(0.3).restart();

    drag(node2);

    // d-k graph
    node3 = node3.data(nodes3, d => d.id);
    node3.exit().remove();
    node3 = node3.enter()
        .append('circle')
        .attr('r', 10)
        .style('fill', d => colors(d.id))
        .style('stroke', d => d3.rgb(colors(d.id)).darker().toString())
        .merge(node3);
    
    node3.append('title').text((d) => d.id)
    
    link3 = link3.data(links3);
    link3.exit().remove();
    link3 = link3.enter()
        .append('line')
        .attr('class', 'link')
        .style('stroke', '#333')
        .style('stroke-width', '4px')
        .merge(link3);
    
    simulation3.nodes(nodes3);
    simulation3.force("link").links(links3);
    simulation3.alphaTarget(0.3).restart();

    drag(node3);
}

const zoom = d3.zoom()
    .on('zoom', () => {
        g.attr("transform", d3.event.transform);
        g2.attr("transform", d3.event.transform);
        g3.attr("transform", d3.event.transform);
    })

zoom(svg)