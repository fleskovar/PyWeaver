from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from Nodes import Node, Block

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

root = Node()

@socketio.on('new_node')
def add_new_node(id):
    global root
    n1 = Block(root, id)  
    print 'log: create node'  
    # emit('responseEvent', {'data': 'got it!'})

@socketio.on('edit_node_code')
def edit_node_code(data):
    global root

    id = data['id']
    code = data['code']

    b = root.blocks[id]
    b.parse_code(code)

    print 'log: parsed'
    print code

    print b.output_vars
    print b.input_vars
    emit('change_node_input_ports', b.input_vars, json=True)
    emit('change_node_output_ports', b.output_vars)

@socketio.on('make_connection')
def make_connection(data):
    global root

@socketio.on('undo_connection')
def undo_connection(data):
    global root

@socketio.on('run')
def run(data):
    global root

if __name__ == '__main__':
    socketio.run(app, host='localhost', port=5000)