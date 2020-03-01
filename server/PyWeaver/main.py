from flask import Flask, json
from flask_socketio import SocketIO, emit
import sys
from copy import deepcopy
import webbrowser
import os, inspect, shutil
from code import InteractiveConsole
from io import StringIO
from contextlib import redirect_stdout

# For local

from Graph import Graph
from results_encoder import CustomJSONEncoder
from LibraryManager import LibraryManager
from model_manager import create_node, load_xml
from refactor_magic import tabs_to_space, functionalize, vectorize
"""
# For release

from PyWeaver.Graph import Graph
from PyWeaver.results_encoder import CustomJSONEncoder
from PyWeaver.LibraryManager import LibraryManager
from PyWeaver.model_manager import create_node, load_xml
from PyWeaver.refactor_magic import tabs_to_space, functionalize, vectorize
"""

# Flask server app
app = Flask(__name__, static_url_path='')
app.json_encoder = CustomJSONEncoder
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, json=json, cors_allowed_origins="*")

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/node_viewer')
def view_node():
    return app.send_static_file('node_viewer.html')

@app.route('/get_node_info/<node_id>')
def retrieve_node_data(node_id):
    """
    Method used by the Node Viewer window to retrieve node's UI and Python code.
    This should be called upon
    """
    global graph_root

    node = graph_root.nodes[node_id]

    node_data = dict()
    node_data['ui'] = node.ui_code
    node_data['script'] = node.ui_script
    node_data['code'] = tabs_to_space(node.code)  # Makes sure code is indented with spaces
    node_data['scope'] = node.scope

    return_data = dict()
    return_data['ui_data'] = node_data
    
    node_vars = get_node_data(node_id)
    
    return_data['data'] = node_vars

    return return_data

@socketio.on('get_node_view_update')
def node_display_update(node_id):
    node_vars = get_node_data(node_id)
    return node_vars


@socketio.on('execute_console')
def execute_console(code):
    global python_console

    f = StringIO()
    with redirect_stdout(f):
        python_console.runcode(code)
    result = f.getvalue()
    
    emit('print_to_console', result)
    

def get_node_data(node_id):
    """
    This method takes a node id and return a dictionary with all the input, output variable and their values.
    This is used for showing the node display in a separate window.
    """
    global graph_root
    

    node = graph_root.nodes[node_id]
    input_vars = node.input_vars_data
    output_vars = node.output_vars

    r = dict()

    # Loop through the input vars and find their values in the store.
    # We first need to find the id of the source node and then find that variable in the data store.
    # The inputs of the node contain the source node and the name of the variable.
    for v in input_vars:
        # TODO: Decide what happens when this becomes a multiple connection input. List of values?
        # How does this work in the regular UI?
        val = []
        
        for con in input_vars[v]:
            source_node = con[0]
            var_name = con[1]
            val.append(graph_root.store[source_node][var_name].value)


        if len(val) == 1:
            # If only one value is inside (because this input has only one connection)
            # Unpack the value and avoid returning a list
            val = val[0]
        
        r[v] = val  # Can either return a list (if multiple connections are made) or a single value

    # Loop through the output variables and the find their values in the store.
    # The variables can easily be found in the store because we already know the id of the node containing them
    for v in output_vars:        
        r[v] = graph_root.store[node_id][v].value

    return r

@socketio.on('get_node_view_data')
def get_node_view_data(data):
    """
    Method used by the Node Viewer window to retrieve node's UI and Python code.
    """
    global graph_root
    node_id = data['node_id']

    node = graph_root.nodes[node_id]

    node_data = dict()
    node_data['ui'] = node.ui_code
    node_data['script'] = node.ui_script
    node_data['code'] = tabs_to_space(node.code)  # Makes sure code is indented with spaces
    node_data['scope'] = node.scope

    return node_data

def set_node_client_code(node_id, code, code_type='code'):
    
    data = dict()
    data['code'] = code
    data['node_id'] = node_id
    
    if code_type == 'code':
        emit('set_node_client_code', data)  # Send session id to the client
    elif code_type == 'ui':
        emit('set_node_client_ui', data)  # Send session id to the client
    elif code_type == 'ui_script':
        emit('set_node_client_ui_script', data)  # Send session id to the client

@app.route('/config')
def get_config_file():
    cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    config_path = os.path.join(cwd, 'client_pref.json')
    f = open(config_path)
    config = f.read()
    f.close()
    return config


@socketio.on('new_node_from_code')
def add_new_node_from_code(node_data):
    global graph_root
    template = dict()  # Set empty template

    template['code'] = node_data['code']
    template['display_code'] = node_data['display_code']
    template['display_act_code'] = node_data['display_act_code']

    create_node(graph_root, template)

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
    graph_root.nodes[node_id].set_dirty()

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

@socketio.on('refactor_to_function')
def refactor_to_function(refactor_data):
    global graph_root
    template = dict()  # Set empty template
    node_id = refactor_data['id']

    code = functionalize(refactor_data['code'], refactor_data['inner_vars'])  # Applies refactor magic

    data = dict()
    data['id'] = node_id
    data['code'] = code
    data['ui_code'] = refactor_data['ui_code']
    data['ui_script'] = refactor_data['ui_script']

    edit_node_code(data)
    set_node_client_code(node_id, code)

@socketio.on('edit_node_code')
def edit_node_code(data):
    global graph_root

    id = data['id']
    code = tabs_to_space(data['code'])  # Makes sure code is indented with spaces
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
    # TODO: this should return the whole variable data (including type) so that the display can use it
    global graph_root
    global python_console
    
    sucess = graph_root.execute(scope_data)

    r = dict()
    for n in graph_root.nodes:
        rr = dict()
        for v in graph_root.store[n]:
            var_obj = graph_root.store[n][v]
            # Transforms result into JSON safe data
            rr[v] = var_obj.value
        r[n] = rr

    python_console.__dict__['locals']['_data'] = r  # Inject results into console's scope

    emit('graphExecuted', None, broadcast=True)

    return r


# TODO: implement this so that it return all the values of the variables in a node
# this is important for the display pop-up
@socketio.on('get_node_variables')
def get_node_variables(node_id):
    global graph_root

    r = dict()
    for n in graph_root.nodes:
        rr = dict()
        for v in graph_root.store[n]:
            var_obj = graph_root.store[n][v]
            # Transforms result into JSON safe data
            rr[v] = var_obj.value
        r[n] = rr
    return r


@socketio.on('reset')
def reset():
    global graph_root
    global library
    global init_modules
    global init_path
    global python_console

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
    python_console = InteractiveConsole()


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

#def execute_on_console():
#    if console_scope is None:
#        self.func.__globals__['display'] = scope_data


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
results = dict()
python_console = InteractiveConsole()


def start():
    print('Started at localhost:5000. Make sure to use Chrome')
    client_url = "http://localhost:5000"
    browser = webbrowser.get()
    browser.open_new(client_url)
    socketio.run(app, host='localhost', port=5000)


if __name__ == '__main__':    
    start()
