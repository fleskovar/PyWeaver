from flask_socketio import emit
from collections import OrderedDict
from PyWeaver.code_parsing import parse_function
import traceback
import re
from copy import deepcopy
import sys, os


class Node(object):

    def __init__(self, parent_node, id, code=None):

        self.parent_node = parent_node
        self.display = None  # TODO: Implement display option for web client
        self.dirty = True  # This property determines if the node needs to be recomputed
        self.scope = dict()
        self.code = code
        self.id = id
        self.output_vars_data = OrderedDict()
        self.func_name = None
        self.func = None

        self.input_vars = []
        self.input_vars_named = OrderedDict()
        self.input_vars_data = OrderedDict()
        self.output_vars = []

        if code is not None:
            self.parse_code(code)

    def parse_code(self, code):
        self.set_dirty()
        self.code = code
        success, func_name, input_vars, input_vars_named, input_vars_data, output_vars = parse_function(code)
        self.func_name = func_name
        self.func_dict = {}
        
        compile_success = False
        try:
            exec(code, self.func_dict)
            compile_success = True
        except Exception as e:
            print(e)            
        
        if compile_success:
            self.func = self.func_dict[func_name]
            self.func.__globals__['display'] = {}

            if len(input_vars) < len(self.input_vars):
                # I could also check that if the smaller new input has some variables in common
                # with the previous input, then I should only delete the extra variables
                self.input_vars_data = OrderedDict()
            elif input_vars[:len(self.input_vars)] != self.input_vars:
                self.input_vars_data = OrderedDict()

            # if(self.input_vars != input_vars):
            #    self.input_vars_data = dict()

            if len(output_vars) < len(self.output_vars):
                # I could also check that if the smaller new input has some variables in common
                # with the previous input, then I should only delete the extra variables
                self.output_vars_data = OrderedDict()
            elif output_vars[:len(self.output_vars)] != self.output_vars:
                self.output_vars_data = OrderedDict()

            # if(self.output_vars != output_vars):
            #    self.output_vars_data = dict()

            self.input_vars = input_vars
            self.input_vars_named = input_vars_named

            # TODO: check if I should delete this
            # self.input_vars_data = input_vars_data

            self.output_vars = output_vars
            
            self.results = {}
            # self.input_results = {}

            self.results = OrderedDict()

            for o in output_vars:
                self.results[o] = None

            # for o in input_vars:
            #    self.input_results[o] = None

    def has_downstream(self):
        val = len(self.output_vars_data.keys()) > 0
        return val

    def execute(self, scope_data):
        sucess_run = True # Determines if the code was sucessfully executed
        
        #Inject display's scope
        if self.func is not None:
            self.func.__globals__['display'] = scope_data
            self.scope = scope_data
            # TODO: Check if function has outputs
            if len(self.input_vars) == 0:
                if len(self.output_vars) != 0:
                    try:
                        output_vals = self.func()
                    except Exception as e:
                        print(e)
                        sucess_run = False
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        self.send_error_to_server(exc_type, exc_obj, exc_tb)
                else:
                    try:
                        self.func()
                    except Exception as e:
                        print(e)
                        sucess_run = False
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        self.send_error_to_server(exc_type, exc_obj, exc_tb)
            else:
                # Fetch input values from parent's node scope
                inputs, named_inputs = self.get_inputs()

                if len(inputs) == len([i for i in self.input_vars_named if self.input_vars_named[i] is False]):
                    # Checks if the total ammount unnamed inputs given to the func are enough to run the calculation
                    if len(self.output_vars) != 0:
                        try:
                            output_vals = self.func(*inputs, **named_inputs)
                        except Exception as e:
                            print(e)
                            sucess_run = False
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            self.send_error_to_server(exc_type, exc_obj, exc_tb)

                    else:
                        self.func(*inputs)
                else:
                    # Cannot exec because we dont have enough inputs
                    overlay_data = {}
                    overlay_data['node_id'] = self.id
                    overlay_data['overlay_type'] = 'warning'
                    emit('set_node_overlay', overlay_data)

                    sucess_run = False
                    output_vals = None

            if sucess_run:
                if len(self.output_vars) != 0:
                    if isinstance(output_vals, tuple):
                        for i, o in enumerate(self.output_vars):
                            self.results[o] = output_vals[i]
                    else:
                        self.results[self.output_vars[0]] = output_vals
                self.dirty = False

            return sucess_run
        else:
            return False  #No function object found

    def get_inputs(self):
                
        # TODO: Check order of inputs. Somehow, the test version is not working.
        # Inputs are being fed in reverse order
        input_vals = []
        named_input_vals = dict()

        for i in self.input_vars:
            has_default = self.input_vars_named[i]  # Flag that indicates if the var has a default value
            data_list = self.input_vars_data[i] if i in self.input_vars_data else []
            val = None

            if len(data_list) > 0:

                # Fetch input only if connections available

                if len(data_list) == 1:
                    # If only one connection is made to this input, pass it as a value
                    data = data_list[0]
                    node_id = data[0]
                    var_name = data[1]
                    val = self.parent_node.get_var_value(node_id, var_name)                
                elif len(data_list) > 1:
                    # If multiple connections are made to the variable, vectorize it
                    val = []
                    for data in data_list:
                        node_id = data[0]
                        var_name = data[1]
                        result = self.parent_node.get_var_value(node_id, var_name)
                        val.append(result)

                #self.input_results[i] = val # Save the results of the inputs to pass them to the UI

                # TODO: find a better way to handle this: it causes data duplication
                if has_default:
                    named_input_vals[i]=val
                else:
                    input_vals.append(val)

        input_vals = deepcopy(input_vals) # This should make the original inputs immutable
        named_input_vals = deepcopy(named_input_vals)

        return input_vals, named_input_vals

    def connect_output(self, var, target_node, target_var):
        self.parent_node.update_adjacency(self, target_node)
        # TODO: disconnect should undo this
        if target_var not in target_node.input_vars_data:
            # Store connections as a list in case i/o has multiple connections
            target_node.input_vars_data[target_var] = []

        target_node.input_vars_data[target_var].append((self.id, var)) # Bind target's input var to local output
        
        if var not in self.output_vars_data:
            self.output_vars_data[var] = []
        
        self.output_vars_data[var].append((target_node.id, target_var)) # Bind local var to target's var
        
        target_node.set_dirty() # A new connection was made. Should recalc.

    def disconnect_output(self, var, target_id, target_var):
        # Takes an output variable, searches for the corresponding connection and deletes it
        
        conn_data = self.output_vars_data[var]  

        # Search for output var and disconnect it
        target_node = self.parent_node.nodes[target_id] # Get reference of target node     
        
        record_index = target_node.input_vars_data[target_var].index((self.id, var))
        target_node.input_vars_data[target_var].pop(record_index)
        if len(target_node.input_vars_data[target_var]) == 0:
            del target_node.input_vars_data[target_var]
        #del target_node.input_vars_data[target_var] # Delete input connection.
        target_node.set_dirty() # Target lost an input. Should recalc.

        #self.parent_node.remove_fom_adjacency_dict(self.id, target_id) # Remove connection from adjacency dict
        self.parent_node.remove_fom_adjacency_dict(target_id, self.id) 

        
        record_index = self.output_vars_data[var].index((target_id, target_var))
        self.output_vars_data[var].pop(record_index)
        if len(self.output_vars_data[var]) == 0:
            del self.output_vars_data[var]
        #del self.output_vars_data[var] # Delete output local conection reference.

    def set_dirty(self):
        self.dirty = True

        for var in self.output_vars_data:
            # Iterate through all connections
            data = self.output_vars_data[var] # Get the connection data (We are interested in the id of the nodes downstream)
            for d in data:
                self.parent_node.nodes[d[0]].set_dirty() # Propagate dirty state downstream

    def send_error_to_server(self, exc_type, exc_obj, exc_tb):
        error = str(traceback.format_exc())

        try:
            regex_l = re.search('(File "<string>", line )([0-9]*)', error)
            line_num = float(regex_l.group(2))
        except:
            line_num = exc_tb.tb_lineno

        exception = dict()
        exception['id'] = self.id
        exception['line'] = line_num
        exception['error_type'] = str(exc_type)
        exception['error'] = error
        emit('add_error', exception)

        overlay_data = {}
        overlay_data['node_id'] = self.id
        overlay_data['overlay_type'] = 'error'
        emit('set_node_overlay', overlay_data)
