import ast

class Node(object):

    def __init__(self):
        self.scope = None  # TODO: Implement scope
        self.blocks = {}        
        self.edges=[]
        self.adjacency_dict = dict()
        self.terminal_blocks = []  # List of blocks that have no output

    def add_block(self, block):
        block_id = block.id
        self.blocks[block_id] = block
        self.adjacency_dict[block_id] = []

    def connect(self, source_node, target_node):
        self.edges.append((source_node.id, target_node.id))
        self.update_adjacency_dict(source_node.id, target_node.id)
        self.update_adjacency_dict(target_node.id, source_node.id)

    def make_connection(self, source_id, source_var, target_id, target_var):
        source_b = self.blocks[source_id]
        target_b = self.blocks[target_id]
        source_b.connect(source_var, target_b, target_var)

    def update_adjacency_dict(self, node_id, neighbor_id):
        if neighbor_id not in self.adjacency_dict[node_id]:
            self.adjacency_dict[node_id].append(neighbor_id)

    def get_var_value(self, block_id, var):
        block = self.blocks[block_id]
        return block.results[var]

    def execute(self):

        blocks = [self.blocks[b] for b in blocks if self.blocks[b].has_downstream]

        for b in self.blocks:
            block_stack = [b.id]
            exec_list = []
            while block_stack:
                current = block_stack.pop()
                for neighbor in self.adjacency_dict[current]:
                    if not neighbor in exec_list:
                        block_stack.append(neighbor)
                exec_list.append(current)

            exec_list = exec_list[::-1]  # Reverse list to get proper execution order

            for id in exec_list:
                exe_block = self.blocks[id]
                if exe_block.dirty:
                    exe_block.execute()

    def build_adjacency_dict(self):
        # TODO: build adjacency dict from edges list
        pass

    def build_execution_order_list(self):
        return None

class Block(object):

    def __init__(self, parent_node, id, code=None, params=dict()):

        self.parent_node = parent_node
        self.display = None  # TODO: Implement display option for web client
        self.dirty = True  # This property determines if the block needs to be recomputed
        self.scope = dict()
        self.code = code
        self.id = id
        self.has_downstream = False
        self.connections = dict()

        self.input_vars = []
        self.input_vars_data = {}
        self.output_vars = []

        if code is not None:
            self.parse_code(code)            

        self.parent_node.add_block(self)        

    def parse_code(self, code, params=dict()):
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
        self.has_downstream = False
        self.connections = dict()

        self.params = params
        self.results = {}

        self.results = dict()

        for o in output_vars:
            self.results[o] = None

        self.dirty = True

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
            block_id = data[0]
            var_name = data[1]
            val = self.parent_node.get_var_value(block_id, var_name)
            input_vals.append(val)
        return input_vals

    def connect(self, var, target_node, target_var):
        self.parent_node.connect(self, target_node)
        # TODO: disconnect should undo this
        # Maybe store reference to target here for undo?
        target_node.input_vars_data[target_var] = (self.id, var)
        self.connections[var] = (target_node.id, target_var)
        target_node.dirty = True

    def disconnect(self, var):
        conn_data = self.connections[var]
        target_id = conn_data[0]
        target_var = conn_data[1]
        #TODO: make it so that if node is not longer there, delete connection anyways
        self.parent_node.blocks[target_id].connections[target_var] = None
        target_node.dirty = True

if __name__ == '__main__':

    root = Node()
    code_2 = open('func_b.py').read()
    n1 = Block(root, code_2)
    # node_in.execute()
    code = open('func_a.py').read()
    n2 = Block(root, code)
    n1.connect('x', n2, 'x')
    n1.connect('y', n2, 'y')
    root.execute()
