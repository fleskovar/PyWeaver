import ast
from collections import OrderedDict

def parse_function(code):

    input_vars = []
    output_vars = []
    func_name = None
    success = False

    tree = ast.parse(code)  # Parse supplied code into a syntax tree

    funcs = [f for f in tree.body if isinstance(f, ast.FunctionDef)]  # Extract all function declarations

    if len(funcs) == 1:
        # TODO: Catch and raise exception if more than one func declared in body
        # If more than one function was declared in the root of the file, return an error
        func = funcs[0]
        func_name = func.name
        return_statements = [r for r in func.body if isinstance(r, ast.Return)]  # Get all return statements

        # Extract return variables only if there is a return statement
        if len(return_statements) == 1:            
            return_statement = return_statements[0].value
            output_vars = extract_outputs(return_statement)

        # Extract input variables
        input_vars, input_vars_named = extract_inputs(func)

    input_vars_dict = {}
    for i in input_vars:
        # TODO: Determine if input_vars_dict needs to be initialized with None
        input_vars_dict[i] = None

    return success, func_name, input_vars, input_vars_named, input_vars_dict, output_vars


def extract_inputs(function_statement):
    input_vars = []
    input_vars_named = OrderedDict()

    # This number tells us how many unnamed args we have at the begining of the function declaration
    named_offset=len(input_vars) - len(function_statement.args.defaults)

    for i, var in enumerate(function_statement.args.args):
        
        input_vars.append(var.arg)
        
        if i+1 < named_offset:
            input_vars_named[var.arg] = True
        else:
            input_vars_named[var.arg] = False

    return input_vars, input_vars_named


def extract_outputs(return_statement):
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
        if isinstance(return_statement, ast.Name):
            if(return_statement.id != 'None'):
                output_vars.append(return_statement.id)

    return output_vars
