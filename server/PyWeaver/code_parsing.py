import ast


def parse_function(code):

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
            input_vars = extract_inputs(func)
            return_statement = return_statements[0].value
            output_vars = extract_outputs(return_statement)

    input_vars_dict = {}
    for i in input_vars:
        # TODO: Determine if input_vars_dict needs to be initialized with None
        input_vars_dict[i] = None

    return success, func_name, input_vars, input_vars_dict, output_vars


def extract_inputs(function_statement):
    input_vars = []
    for var in function_statement.args.args:
        input_vars.append(var.id)
    return input_vars


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
        output_vars.append(return_statement.id)

    return output_vars
