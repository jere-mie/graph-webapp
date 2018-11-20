## Download
To download as zip simply click on the cloud icon above.

Nodejs and npm is required you can
[download](https://nodejs.org/en/download/) current version.

## Install Dependencies
Once Nodejs and npm is installed and the repository download to a directory. In the directory run, `npm install` to install the dependencies from the package.json file.

Current Dependencies:
* express


## Run
Simply type `node ./server.js` in the directory to the start the server. Navigate to http://localhost:3000 to view the page

## TODO

* Add Home Page, like https://www.desmos.com
* Sample graphs
* Information about chordal graph

Python integrating
* [node-pty?](https://github.com/Microsoft/node-pty)
* [python-shell?](https://github.com/extrabacon/python-shell)

RESTful API
* Request different graphs from server
* Send current graph to check if it correct

Graph
* Fix error when new graph is loaded and lines(paths) do not line up with source nodes
* Allow user to see the clique tree, maybe add histogram in bottom right of the distribution of tress in the graph
* Scroll to zoom in graph

Graph manipulation
* Delete nodes without links
* Delete duplicate links
