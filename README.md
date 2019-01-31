## Download
To download as zip simply click on the cloud icon above.

Nodejs and npm is required you can
[download](https://nodejs.org/en/download/) current version.

## Install Dependencies
Once Nodejs and npm is installed and the repository download to a directory. In the directory run, `npm install` to install the dependencies from the package.json file.

Current Dependencies:
* express
* python-shell
* Python 2.7 installed in the default directory (Windows C:/Python27/python.exe, other /usr/bin/python)


## Run
Simply type `npm start` in the directory to the start the server. Navigate to http://localhost:3000 to view the page

## TODO

* Information about chordal graph

RESTful API
* Send current graph to check if it correct
* [Tutorial](https://medium.com/@purposenigeria/build-a-restful-api-with-node-js-and-express-js-d7e59c7a3dfb)

Graph
* Fix error when new graph is loaded and lines(paths) do not line up with source nodes
* Allow user to see the clique tree, maybe add histogram in bottom right of the distribution of tress in the graph
* Scroll to zoom in graph
* Allow user to upload graph data

Graph manipulation
* Delete nodes without links
* Delete duplicate links
