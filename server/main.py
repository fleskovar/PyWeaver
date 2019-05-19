from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from Nodes import Node, Graph, Session

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
    b.parse_code(code)

    emit('change_node_input_ports', b.input_vars, json=True)
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
def execute():
    global root

    root.execute()

    r = dict()
    for n in root.nodes:
        rr = dict()
        for v in root.nodes[n].results:
            rr[v] = root.nodes[n].results[v]
        r[n] = rr

    return r

if __name__ == '__main__':
    print 'Started'
    socketio.run(app, host='localhost', port=5000)