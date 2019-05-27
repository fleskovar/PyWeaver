from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import sys
from copy import deepcopy

from Nodes import Node
from Graph import Graph
from results_encoder import encode
from LibraryManager import LibraryManager

# Register initial modules that should not be deleted when restarting the server
init_modules = sys.modules.keys()
init_path = deepcopy(sys.path)

# Flask server app
app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

root = Graph()
library = LibraryManager()

@app.route('/')
def root():
    return app.send_static_file('index.html')

@socketio.on('new_node')
def add_new_node(node_id):
    global root

    # TODO: rethink this
    n1 = Node(root, node_id)

@socketio.on('delete_node')
def delete_node(node_id):
    global root
    root.delete_node(node_id)


@socketio.on('connect')
def made_connection():
    global library
    tree = library.get_tree()
    emit('set_library_tree', tree)

@socketio.on('edit_node_code')
def edit_node_code(data):
    global root

    id = data['id']
    code = data['code']

    b = root.nodes[id]
    old_input_vars = b.input_vars
    old_output_vars = b.output_vars
    b.parse_code(code)

    if old_input_vars != b.input_vars:
        # Prevents emitting an event when input didnt change
        emit('change_node_input_ports', b.input_vars, json=True)

    if old_output_vars != b.output_vars:
        # Prevents emitting an event when output didnt change
        emit('change_node_output_ports', b.output_vars)


@socketio.on('make_connection')
def make_connection(data):
    global root
    source_id = data['source_id']
    target_id = data['target_id']
    source_var = data['source_var']
    target_var = data['target_var']

    root.make_connection(source_id, source_var, target_id, target_var)


@socketio.on('delete_connection')
def delete_connection(data):
    global root
    source_id = data['source_id']
    source_var = data['source_var']

    target_id = data['target_id']
    target_var = data['target_var']

    root.delete_connection(source_id, source_var, target_id, target_var)


@socketio.on('execute')
def execute(scope_data):
    global root

    print 'Running'
    root.execute(scope_data)

    r = dict()
    for n in root.nodes:
        rr = dict()
        for v in root.nodes[n].results:
            # Transforms result into JSON safe data
            rr[v] = encode(root.nodes[n].results[v])

        r[n] = rr

    print 'Finished'
    return r


@socketio.on('reset')
def reset():
    global root
    global library
    global init_modules
    global init_path

    # Resets module imports
    if 'init_modules' in globals():
        # remove all but initially loaded modules
        for m in sys.modules.keys():
            if m not in init_modules:
                del (sys.modules[m])

    # Resets the path
    sys.path = init_path

    # TODO: Reset declared classes and functions

    # Reset computational graph and library
    root = Graph()
    library = LibraryManager()

@socketio.on('get_template_names')
def get_template_names():
    global library
    return library.get_template_names()

@socketio.on('get_tree')
def get_tree():
    global library
    tree = library.get_tree()
    return tree

@socketio.on('get_template')
def get_template_names(lib_id):
    global library
    return library.get_render(lib_id)

@socketio.on('save_to_library')
def get_template_names(data):
    global library
    path = data['path']
    node_data = data['node_data']

    library.save(path, node_data)

    library = LibraryManager()
    tree = library.get_tree()
    emit('set_library_tree', tree)

if __name__ == '__main__':
    print 'Started'
    socketio.run(app, host='localhost', port=5000)

