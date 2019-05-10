import ast

class Session(object):

    def __init__(self):
        self.graph = Graph()

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
        self.adjacency_dict[node_id] = []

    def update_adjacency(self, source_node, target_node):
        self.edges.append((source_node.id, target_node.id))
        self.update_adjacency_dict(source_node.id, target_node.id)
        self.update_adjacency_dict(target_node.id, source_node.id)

    def make_connection(self, source_id, source_var, target_id, target_var):
        print 'making conn'
        source_b = self.nodes[source_id]
        target_b = self.nodes[target_id]
        source_b.connect_output(source_var, target_b, target_var)

    def delete_connection(self, source_id, source_var):
        node = self.nodes[source_id]
        node.disconnect_output(source_var)
    
    def update_adjacency_dict(self, node_id, neighbor_id):
        if neighbor_id not in self.adjacency_dict[node_id]:
            self.adjacency_dict[node_id].append(neighbor_id)

    def remove_adjacency_dict(self, node_id, neighbor_id):        
        self.adjacency_dict[node_id].remove(neighbor_id)
        self.adjacency_dict[neighbor_id].remove(node_id)

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

    def __init__(self, parent_node, id, code=None, params=dict()):

        self.parent_node = parent_node
        self.display = None  # TODO: Implement display option for web client
        self.dirty = True  # This property determines if the node needs to be recomputed
        self.scope = dict()
        self.code = code
        self.id = id
        self.connections = dict()

        self.input_vars = []
        self.input_vars_data = {}
        self.output_vars = []

        if code is not None:
            self.parse_code(code)            

        self.parent_node.add_node(self)        

    def parse_code(self, code, params=dict()):
        self.set_dirty()
        self.code = code
        success, func_name, input_vars, input_vars_data, output_vars = self.parse_function(code)  
        self.func_name = func_name
        self.func_dict = {}
        exec code in self.func_dict
        self.func = self.func_dict[func_name]
        self.func.__globals__['scope'] = self.scope
        self.input_vars = input_vars
        self.input_vars_data = input_vars_data
        self.output_vars = output_vars        
        self.connections = dict()

        self.params = params
        self.results = {}

        self.results = dict()

        for o in output_vars:
            self.results[o] = None

    def has_downstream(self):
        val = len(self.connections.keys()) > 0
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
        input_vals = []
        for i in self.input_vars_data:
            data = self.input_vars_data[i]
            node_id = data[0]
            var_name = data[1]
            val = self.parent_node.get_var_value(node_id, var_name)
            input_vals.append(val)
        return input_vals

    def connect_output(self, var, target_node, target_var):
        self.parent_node.update_adjacency(self, target_node)
        # TODO: disconnect should undo this        
        target_node.input_vars_data[target_var] = (self.id, var) # Bind target's input var to local output
        self.connections[var] = (target_node.id, target_var) # Bind local var to target's var
        target_node.set_dirty() # A new connection was made. Should recalc.

    def disconnect_output(self, var):
        #TODO: make it so that if node is not longer there, delete connection anyways
        conn_data = self.connections[var]
        target_id = conn_data[0]
        target_var = conn_data[1]

        # Search for output var and disconnect it
        target_node = self.parent_node.nodes[target_id] # Get reference of target node     
        del target_node.input_vars_data[target_var] # Delete connection.
        target_node.set_dirty() # Target lost an input. Should recalc.

        self.parent_node.remove_adjacency_dict(self.id, target_id) # Remove connection from adjacency dict

        del self.connections[var] # Dele local conection reference.

    def set_dirty(self):
        self.dirty = True

        for var in self.connections:
            # Iterate through all connections
            data = self.connections[var] # Get the connection data (We are interested in the id of the nodes downstream)
            self.parent_node.nodes[data[0]].set_dirty() # Propagate dirty state downstream

if __name__ == '__main__':

    root = Graph()
    code_2 = open('func_b.py').read()
    n1 = Node(root, code_2)
    # node_in.execute()
    code = open('func_a.py').read()
    n2 = Node(root, code)
    n1.connect_output('x', n2, 'x')
    n1.connect_output('y', n2, 'y')
    root.execute()
