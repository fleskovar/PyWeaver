# PyWeaver
PyWeaver is a visual code editor for Python 3 that leverages web technologies. It is inspired by Jupyter Notebook and Simulink. The project is under development.

## Installation
```
pip install pyweaver
```
To run the app simply open a cmd and:
```
pyweaver
```

![pyweaver_example](https://user-images.githubusercontent.com/6884660/58805403-65e72780-85ea-11e9-9d7f-4eb8cb5aeb45.PNG)

## Motivation
I spend most of my time analyzing data (mostly time series) of chemical process plants. I wanted a tool that optimizes the workflow of importing, cleaning and analyzing data by expliciting the relationship of the variables involved and defining the flow of information.
I wanted the tool to have enough flexibility to display different type of plots and UI components and perform any kind of calculation.

Ultimately, PyWeaver will have the functionality to store and grow a library of computational nodes that users will be able to drag & drop to define their workflows. They will also be able to easily develop their own nodes to fit their specific needs.

## Installation
If you want to run the current development version:
Clone the repo, cd into client, npm i and npm run serve.
Also, cd into server, run python main.py.

This will be improved shortly.

![pyweaver_1](https://user-images.githubusercontent.com/6884660/57988776-70d97e00-7a68-11e9-9bb5-7f304aec0bac.PNG)

## How it works

Each computational node is defined by a Python function, an HTML snippet that determines what is displayed in the UI and a Java Script object containing any functions needed by the UI. All the code is introduced via the web client and processed by the server:

Python function:
![pyweaver_2](https://user-images.githubusercontent.com/6884660/57988857-5eac0f80-7a69-11e9-94e3-8884114598fd.PNG)
The server analyzes the code, finds the inputs and outputs of each function and creates the sockets in the UI to specify how to connect the variables.

HTML Display:
![pyweaver_3](https://user-images.githubusercontent.com/6884660/57988860-68357780-7a69-11e9-8ee4-18c6ad9742a3.PNG)
PyWeaver leverages the power of Vue.js, mxgraph, codemirror and Vuetify. I am currently working on integrating Plotly.

Result:
![pyweaver_4](https://user-images.githubusercontent.com/6884660/57988881-9dda6080-7a69-11e9-92cd-19dca7ef42b1.PNG)
