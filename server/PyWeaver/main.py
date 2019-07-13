from flask import Flask, json
from flask_socketio import SocketIO, emit
import sys
from copy import deepcopy
import webbrowser
import os, inspect, shutil

from Graph import Graph
from results_encoder import CustomJSONEncoder
from LibraryManager import LibraryManager
from model_manager import create_node, load_xml


# Flask server app
app = Flask(__name__, static_url_path='')
app.json_encoder = CustomJSONEncoder
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, json=json)

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/node_viewer')
def view_node():
    return app.send_static_file('node_viewer.html')


@app.route('/config')
def get_config_file():
    cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    config_path = os.path.join(cwd, 'client_pref.json')
    f = open(config_path)
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

@socketio.on('set_output_type')
def set_output_type(data):
    global graph_root

    node_id = data['id']
    var_name = data['var_name']
    is_val = data['is_val']

    graph_root.nodes[node_id].isOutputVal[var_name] = is_val


@socketio.on('delete_node')
def delete_node(node_id):
    global graph_root
    graph_root.delete_node(node_id)


@socketio.on('connect')
def client_connected():
    global library
    global graph_root
    tree = library.get_tree()
    
    send_library_tree_data()

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
    ui_code = data['ui_code']
    ui_script = data['ui_script']

    b = graph_root.nodes[id]
    old_input_vars = b.input_vars
    old_output_vars = b.output_vars
    
    # Adds python, html and javascript code to the node
    b.parse_code(code)
    b.ui_code = ui_code
    b.ui_script = ui_script

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

    connection_name = ''
    # connection_name = source_id + '-' + source_var

    graph_root.make_connection(source_id, source_var, target_id, target_var, connection_name)


@socketio.on('delete_connection')
def delete_connection(data):
    global graph_root
    source_id = data['source_id']
    source_var = data['source_var']

    target_id = data['target_id']
    target_var = data['target_var']

    graph_root.delete_connection(source_id, source_var, target_id, target_var)
    

@socketio.on('rename_connection')
def rename_connection(data):
    global graph_root
    source_id = data['source_id']
    source_var = data['source_var']

    target_id = data['target_id']
    target_var = data['target_var']

    name = data['name']

    graph_root.rename_connection(source_id, source_var, target_id, target_var, name)


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

def send_library_tree_data():
    global library
    tree, calcs_list = library.get_tree()

    data={
        'tree': tree,
        'calcs': calcs_list
    }

    emit('set_library_tree', data)

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
    overwrite = data['overwrite']

    library.save(path, node_data, overwrite)

    library = LibraryManager()
    tree = library.get_tree()
    
    send_library_tree_data()


@socketio.on('new_folder')
def new_folder(folder_data):
    global library
    folder_path = folder_data['path']
    folder_name = folder_data['name']
    library.new_folder(folder_path, folder_name)

    library = LibraryManager()
    tree = library.get_tree()
    
    send_library_tree_data()


@socketio.on('delete_folder')
def delete_folder(path):
    global library    
    library.delete_folder(path)

    library = LibraryManager()
    tree = library.get_tree()
    
    send_library_tree_data()


@socketio.on('rename_folder')
def rename_folder(folder_data):
    global library    
    folder_path = folder_data['path']
    folder_name = folder_data['name']
    library.rename_folder(folder_path, folder_name)

    library = LibraryManager()
    tree = library.get_tree()
    
    send_library_tree_data()

@socketio.on('get_library')
def get_library():
    global library    
    pass

@socketio.on('refresh_library')
def refresh_library():
    global library
    library = LibraryManager()    
    send_library_tree_data()

@socketio.on('load_model')
def load_model(xml):
    global graph_root
    graph_root = Graph()
    emit('force_session_id', graph_root.session_id)  # Force a new session id into the UI
    load_xml(graph_root, xml)
    graph_root.xmlModel = xml

@socketio.on('save_config_file')
def save_config_file(xml):
    cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    config_path = os.path.join(cwd, 'client_pref.json')
    f = open(config_path, 'w')
    f.write(xml)
    f.close()


@socketio.on('get_node_display')
def get_node_display(data):
    global graph_root

    node_id = data['id']

    node = graph_root.nodes[node_id]

    ui_code = node.ui_code
    ui_script = node.ui_script
    ui_scope = node.scope

    return {'ui': ui_code, 'script': ui_script, 'scope': ui_scope}
    

# Register initial modules that should not be deleted when restarting the server
init_modules = sys.modules.keys()
init_path = deepcopy(sys.path)
graph_root = Graph()
library = LibraryManager()


def start():
    print('Started at localhost:5000. Make sure to use Chrome')
    client_url = "http://localhost:5000"
    browser = webbrowser.get()
    browser.open_new(client_url)
    socketio.run(app, host='localhost', port=5000)



if __name__ == '__main__':
    start()
