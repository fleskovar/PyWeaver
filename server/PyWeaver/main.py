from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import sys

from Nodes import Node
from Graph import Graph
from results_encoder import encode

# Register initial modules that should not be deleted when restarting the server
init_modules = sys.modules.keys()

# Flask server app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

root = Graph()

@socketio.on('new_node')
def add_new_node(id):
    global root
    n1 = Node(root, id)

@socketio.on('delete_node')
def delete_node(node_id):
    global root
    root.delete_node(node_id)

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
    global init_modules

    if globals().has_key('init_modules'):
        # remove all but initially loaded modules
        for m in sys.modules.keys():
            if m not in init_modules:
                del (sys.modules[m])

    root = Graph()

if __name__ == '__main__':
    print 'Started'
    socketio.run(app, host='localhost', port=5000)