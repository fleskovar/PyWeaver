from flask import Flask, json
from flask_socketio import SocketIO, emit
import sys
from copy import deepcopy

from PyWeaver.Graph import Graph
from PyWeaver.results_encoder import CustomJSONEncoder
from PyWeaver.LibraryManager import LibraryManager
from PyWeaver.model_manager import create_node, load_xml


# Flask server app
app = Flask(__name__, static_url_path='')
app.json_encoder = CustomJSONEncoder
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, json=json)

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/config.json')
def get_config_file():
    f = open('client_pref.json')
    config = f.read()
    f.close()
    return config


@socketio.on('new_empty_node')
def add_new_node():
    global graph_root
    template = dict()  # Set empty template

    template['code'] = ''
    template['display_code'] = 'New Node'
    template['display_act_code'] = '{}'

    create_node(graph_root, template)


@socketio.on('load_node')
def load_node(lib_id):
    global library
    global graph_root
    template = library.get_render(lib_id)

    if template is not None:
        # If template was found
        create_node(graph_root, template)

    


@socketio.on('delete_node')
def delete_node(node_id):
    global graph_root
    graph_root.delete_node(node_id)


@socketio.on('connect')
def client_connected():
    global library
    global graph_root
    tree = library.get_tree()
    emit('set_library_tree', tree)
    emit('sync_session', graph_root.session_id)  # Send session id to the client

@socketio.on('sync_model')
def sync_model(model_data):
    global graph_root

    if model_data['session_id'] == graph_root.session_id:
        graph_root.xmlModel =  model_data['xml']
    else:
        # If session_ids dont match, resync
        emit('sync_session', graph_root.session_id)  # Send session id to the client

@socketio.on('request_model')
def model_request():
    global graph_root

    if graph_root.xmlModel is not None:
        xml = graph_root.xmlModel
        session_id = graph_root.session_id
        graph_root = Graph(session_id=session_id)
        load_xml(graph_root, xml)  # Load and push model into UI


@socketio.on('edit_node_code')
def edit_node_code(data):
    global graph_root

    id = data['id']
    code = data['code']

    b = graph_root.nodes[id]
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
    global graph_root
    source_id = data['source_id']
    target_id = data['target_id']
    source_var = data['source_var']
    target_var = data['target_var']

    graph_root.make_connection(source_id, source_var, target_id, target_var)


@socketio.on('delete_connection')
def delete_connection(data):
    global graph_root
    source_id = data['source_id']
    source_var = data['source_var']

    target_id = data['target_id']
    target_var = data['target_var']

    graph_root.delete_connection(source_id, source_var, target_id, target_var)


@socketio.on('execute')
def execute(scope_data):
    global graph_root

    graph_root.execute(scope_data)

    r = dict()
    for n in graph_root.nodes:
        rr = dict()
        for v in graph_root.nodes[n].results:
            # Transforms result into JSON safe data
            rr[v] = graph_root.nodes[n].results[v]
        r[n] = rr
    return r


@socketio.on('reset')
def reset():
    global graph_root
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
    graph_root = Graph()
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

@socketio.on('save_to_library')
def save_to_library(data):
    global library
    path = data['path']
    node_data = data['node_data']

    library.save(path, node_data)

    library = LibraryManager()
    tree = library.get_tree()
    emit('set_library_tree', tree)


@socketio.on('new_folder')
def new_folder(folder_data):
    global library
    folder_path = folder_data['path']
    folder_name = folder_data['name']
    library.new_folder(folder_path, folder_name)

    library = LibraryManager()
    tree = library.get_tree()
    emit('set_library_tree', tree)


@socketio.on('delete_folder')
def delete_folder(path):
    global library    
    library.delete_folder(path)

    library = LibraryManager()
    tree = library.get_tree()
    emit('set_library_tree', tree)


@socketio.on('rename_folder')
def rename_folder(folder_data):
    global library    
    folder_path = folder_data['path']
    folder_name = folder_data['name']
    library.rename_folder(folder_path, folder_name)

    library = LibraryManager()
    tree = library.get_tree()
    emit('set_library_tree', tree)


@socketio.on('refresh_library')
def refresh_library():
    global library
    library = LibraryManager()
    tree = library.get_tree()
    emit('set_library_tree', tree)

@socketio.on('load_model')
def load_model(xml):
    global graph_root
    graph_root = Graph()
    emit('force_session_id', graph_root.session_id)  # Force a new session id into the UI
    load_xml(graph_root, xml)
    graph_root.xmlModel = xml

@socketio.on('save_config_file')
def save_config_file(xml):
    f = open('client_pref.json', 'w')
    f.write(xml)
    f.close()
    

# Register initial modules that should not be deleted when restarting the server
init_modules = sys.modules.keys()
init_path = deepcopy(sys.path)

graph_root = Graph()
library = LibraryManager()

if __name__ == '__main__':
    print('Started')
    socketio.run(app, host='localhost', port=5000)

