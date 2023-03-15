let nodes = []
let lastNodeId = 0
let links = []

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
fileName = "N4E4/chordalGraph.json"
importData(fileName);

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
            // .attr("marker-end", "url(#end)"); // also for adding arrows
        node
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

function restart() {
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
}

const zoom = d3.zoom()
    .on('zoom', () => g.attr("transform", d3.event.transform))

zoom(svg)