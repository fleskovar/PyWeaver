import ast
from collections import OrderedDict

class Session(object):

    def __init__(self):
        self.graph = Graph()
        self.modelXML = None # Server's copy of mxgraph's model xml
        self.key = '' # Random key to identify session. If server's session is different to UI's session, resync

class Graph(object):

    def __init__(self):
        self.scope = None  # TODO: Implement scope
        self.nodes = {}        
        self.edges=[]
        self.adjacency_dict = dict()
        self.terminal_nodes = []  # List of nodes that have no output

    def add_node(self, node):
        node_id = node.id
        self.nodes[node_id] = node
        self.adjacency_dict[node_id] = dict()

    def delete_node(self, node_id):
        # Should add a check here to clear all i/o in the node just in case UI does not
        # properly trigger the deletion of all variables
        del self.nodes[node_id]

    def update_adjacency(self, source_node, target_node):
        self.edges.append((source_node.id, target_node.id))
        #self.add_to_adjacency_dict(source_node.id, target_node.id)

        # By only storing these connections in the adjacency dict, the traversal algorithm doesn't go upstream.
        # This ensures that all nodes are computed in the correct order.
        self.add_to_adjacency_dict(target_node.id, source_node.id)

    def make_connection(self, source_id, source_var, target_id, target_var):
        print 'making conn'
        source_b = self.nodes[source_id]
        target_b = self.nodes[target_id]
        source_b.connect_output(source_var, target_b, target_var)

    def delete_connection(self, source_id, source_var, target_id, target_var):
        node = self.nodes[source_id]
        node.disconnect_output(source_var, target_id, target_var)
    
    def add_to_adjacency_dict(self, node_id, neighbor_id):
        if neighbor_id not in self.adjacency_dict[node_id]:
            self.adjacency_dict[node_id][neighbor_id] = 1
        else:
            self.adjacency_dict[node_id][neighbor_id] += 1

    def remove_fom_adjacency_dict(self, node_id, neighbor_id):   
        if neighbor_id in self.adjacency_dict[node_id]:
            self.adjacency_dict[node_id][neighbor_id] -= 1

        if self.adjacency_dict[node_id][neighbor_id] <= 0:
            del self.adjacency_dict[node_id][neighbor_id]

    def get_var_value(self, node_id, var):
        node = self.nodes[node_id]
        return node.results[var]

    def execute(self):

        node_ids = [self.nodes[b].id for b in self.nodes if self.nodes[b].has_downstream()==False]

        for b_id in node_ids:
            node_stack = [b_id]
            exec_list = []
            while node_stack:
                current = node_stack.pop()
                for neighbor in self.adjacency_dict[current]:
                    # If neighbor is a key of the adjacency dict of "current id"
                    if not neighbor in exec_list:
                        node_stack.append(neighbor)
                exec_list.append(current)

            exec_list = exec_list[::-1]  # Reverse list to get proper execution order

            for id in exec_list:
                exe_node = self.nodes[id]
                if exe_node.dirty:
                    exe_node.execute()

    def build_adjacency_dict(self):
        # TODO: build adjacency dict from edges list
        pass

    def build_execution_order_list(self):
        # TODO: part of the execute method should be refactored here
        return None

class Node(object):

    def __init__(self, parent_node, id, code=None, params=OrderedDict()):

        self.parent_node = parent_node
        self.display = None  # TODO: Implement display option for web client
        self.dirty = True  # This property determines if the node needs to be recomputed
        self.scope = dict()
        self.code = code
        self.id = id
        self.output_vars_data = OrderedDict()

        self.input_vars = []
        self.input_vars_data = OrderedDict()
        self.output_vars = []

        if code is not None:
            self.parse_code(code)            

        self.parent_node.add_node(self)        

    def parse_code(self, code, params=OrderedDict()):
        self.set_dirty()
        self.code = code
        success, func_name, input_vars, input_vars_data, output_vars = self.parse_function(code)  
        self.func_name = func_name
        self.func_dict = {}
        exec code in self.func_dict
        self.func = self.func_dict[func_name]
        self.func.__globals__['scope'] = self.scope
        

        if len(input_vars) < self.input_vars:
            # I could also check that if the smaller new input has some variables in common
            # with the previous input, then I should only delete the extra variables
            self.input_vars_data = OrderedDict()
        elif input_vars[:len(self.input_vars)] != self.input_vars:
            self.input_vars_data = OrderedDict()

        #if(self.input_vars != input_vars):
        #    self.input_vars_data = dict()

        if len(output_vars) < self.output_vars:
            # I could also check that if the smaller new input has some variables in common
            # with the previous input, then I should only delete the extra variables
            self.output_vars_data = OrderedDict()
        elif output_vars[:len(self.output_vars)] != self.output_vars:
            self.output_vars_data = OrderedDict()

        #if(self.output_vars != output_vars):
        #    self.output_vars_data = dict()

        self.input_vars = input_vars

        # TODO: check if I should delete this
        #self.input_vars_data = input_vars_data
        
        self.output_vars = output_vars

        self.params = params
        self.results = {}
        #self.input_results = {}

        self.results = OrderedDict()

        for o in output_vars:
            self.results[o] = None

        #for o in input_vars:
        #    self.input_results[o] = None

    def has_downstream(self):
        val = len(self.output_vars_data.keys()) > 0
        return val

    def parse_function(self, code):

        input_vars = []
        output_vars = []
        func_name = None
        success = False

        tree = ast.parse(code)  # Parse supplied code into a syntax tree

        funcs = [f for f in tree.body if isinstance(f, ast.FunctionDef)]  # Extract all function declarations

        if len(funcs) == 1:
            #  If more than one function was declared in the root of the file, return an error
            func = funcs[0]
            func_name = func.name
            return_statements = [r for r in func.body if isinstance(r, ast.Return)]  # Get all return statements

            if len(return_statements) == 1:
                input_vars = self.extract_inputs(func)
                return_statement = return_statements[0].value
                output_vars = self.extract_outputs(return_statement)

        #TODO: remember why the fuck I am doing this
        input_vars_dict = {}
        for i in input_vars:
            input_vars_dict[i] = None

        return success, func_name, input_vars, input_vars_dict, output_vars

    def extract_inputs(self, function_statement):
        input_vars = []
        for var in function_statement.args.args:
            input_vars.append(var.id)
        return input_vars

    def extract_outputs(self, return_statement):
        output_vars = []

        fields = return_statement._fields

        if 'elts' in fields:
            # Return statement returns more than one value
            elts = return_statement.elts
            for e in elts:
                if isinstance(e, ast.Name):
                    output_vars.append(e.id)
        else:
            # Return statement returns only one value
            output_vars.append(return_statement.id)

        return output_vars

    def execute(self):

        # TODO: Check if function has outputs
        if len(self.input_vars) == 0:
            if len(self.output_vars) != 0:
                output_vals = self.func()
            else:
                self.func()
        else:
            # Fetch input values from parent's node scope
            inputs = self.get_inputs()
            if len(self.output_vars) != 0:
                output_vals = self.func(*inputs)
            else:
                self.func(*inputs)

        if len(self.output_vars) != 0:
            if isinstance(output_vals, tuple):
                for i, o in enumerate(self.output_vars):
                    self.results[o] = output_vals[i]
            else:
                self.results[self.output_vars[0]] = output_vals
        self.dirty = False

    def get_inputs(self):
        # TODO: Find a way to add/inject parameters
        
        # TODO: Check order of inputs. Somehow, the test version is not working.
        # Inputs are being fed in reverse order
        input_vals = []
        for i in self.input_vars_data:
            data_list = self.input_vars_data[i]
            val = None
            if len(data_list) == 1:
                # If only one connection is made to this input, pass it as a value
                data = data_list[0]
                node_id = data[0]
                var_name = data[1]
                val = self.parent_node.get_var_value(node_id, var_name)
                
            else:
                # If multiple connections are made to the variable, vectorize it
                val = []
                for data in data_list:
                    node_id = data[0]
                    var_name = data[1]
                    result = self.parent_node.get_var_value(node_id, var_name)
                    val.append(result)

            #self.input_results[i] = val # Save the results of the inputs to pass them to the UI
            # TODO: find a better way to handle this: it causes data duplication
            input_vals.append(val)
        return input_vals

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
            self.parent_node.nodes[data[0]].set_dirty() # Propagate dirty state downstream