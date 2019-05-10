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
    root.delete_connection(source_id, source_var)

@socketio.on('execute')
def execute():
    global root
    print 'exec'
    root.execute()

    for n in root.nodes:
        for v in root.nodes[n].results:
            print v, root.nodes[n].results[v]

if __name__ == '__main__':
    socketio.run(app, host='localhost', port=5000)