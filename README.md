# A Platform for Generation and Visualization of Graphs

Effortlessly generate and visualize various graph algorithms with our powerful platform

## Prerequesite Software

- Python 3.6 or newer
- Pip(3)

## Running Locally

Follow these steps to run the application on your local device:

1. Clone and enter this repository:

```sh
git clone https://github.com/jere-mie/chordal-graph-webapp
cd chordal-graph-webapp
```

(Alternatively, you can download the source code as a zip)

2. Install libraries via Pip:

```sh
pip3 install -r requirements.txt
```

**Note**: if you're a Windows user, you may need to use `pip` in place of `pip3`.

3. Copy configuration file:

```sh
cp example-config.json config.json
```

At this point, you may want to edit the values in `config.json` though if you're just running the app for development purposes, this won't be necessary.

4. Run the application:

```sh
python3 server.py
```
**Note**: if you're a Windows user, you may need to use `py` instead of `python3`.

This will start the development server, and you can access the web application via [localhost:5000](http://localhost:5000).

## File Structure

Here's a quick rundown on the file structure of the application and what each file/folder is for:

- 📂static/
  - this folder contains all static assets used by the application. This includes CSS, graph JSON data, images, Javascript, and PDFs
- 📂templates/
  - this folder contains all of the HTML templates used to create the webpages for the front end.
  - `layout.html` is the main template that all webpages extend.
  - `graph-template.html` is the template that all of the graph pages extend.
  - other template files are for the individual pages of the website.
- 📃example-config.json
  - this file shows developers what format the configuration file `config.json` should be in. It defines which port the application should run on, as well as the secret key used by the application (this can be anything).
- 📃README.md
  - you're reading this file right now!
- 📃requirements.txt
  - this file tells Pip which libraries are required by the web application
- 📃server.py
  - this contains all of the Flask code to run the server. It sets up the web server and defines the different endpoints.

*All other files should be left over from the old Node.js application*
