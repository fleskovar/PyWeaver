import re

def tabs_to_space(source):
    lines = source.split('\n')
    lines = list(map(lambda l: l.replace('\t', ' '*4), lines))
    new_code = '\n'.join(lines)
    return new_code

def functionalize(source, inner_inputs):
    """
        This function uses various regex expressions to find all uses of display['*'], move them up and then
        encapsulate the original function and return it as the result of a top level function.

        in
        source: string contining the original source code to be refactored
        inner_inputs: list of strings with the variables of the returned function

        out
        new_code: string contining the refactored code of the function
    """
    
    # Transform all tabs into 4 spaces
    source = tabs_to_space(source)

    lines = source.split('\n')

    # Find all function declarations inside the code
    def_rgx = r"def .*"
    def_matches = list(map(lambda l: bool(re.match(def_rgx, l)), lines))
    def_matches_index = [i for i, m in enumerate(def_matches) if m]
    
    # Retrieve the name of the first function declared
    func_name = re.findall(r'def (.*)\(', lines[def_matches_index[0]])[0]  # Retrieves the name of the function
    
    args = re.findall(r'def .*\((.*)\)', lines[def_matches_index[0]])[0].split(',')  # Retrieves the args of the function
    new_args = [ag.strip() for ag in args if ag.strip() not in inner_inputs]  # Keep only args that are not args to the inner func
    
    # Edit inner func def args, leaving only the specified varibles in the inner_inputs list   
    lines[def_matches_index[0]] = re.sub(r'(def .*\()(.*)(\))', r'\1' + ','.join(inner_inputs)+')', lines[def_matches_index[0]])

    # Save the position of all the lines of code above the first function. This is mainly for the imports
    if def_matches_index[0] == 0:
        setup_lines = []
    else:
        setup_lines = lines[0:def_matches_index[0]-1]

    setup_lines.append('')
    lines = lines[def_matches_index[0]:]  # Grab all the rest of the lines

    # Just in case, save the indentation level of the fisrt function (should be 0)
    indent_level = len(lines[def_matches_index[0]].split(' '*4))-1

    # Find all lines of code that use the 'display' dictionary
    # TODO: Change this so that new variables get created where the display reference is and create the new vars at the top
    display_rgx = r"(display\[[\'\"](.*?)[\'\"]\])"
    display_matches = list(map(lambda l: re.findall(display_rgx, l), lines)) # List of lists with all matches
    display_matches_bool = list(map(lambda l: bool(re.findall(display_rgx, l)), lines))
    display_matches_index = [i for i, m in enumerate(display_matches_bool) if m]

    # Make new lines declarations
    new_display_vars = dict()
    replaced_lines = []
    for i, m in enumerate(display_matches):
        line = lines[i]
        for d in m:
            display_ref = d[0]  # display['var']
            replace = '__'+d[1]  # __var 
            pattern = r'display\[(.*?)\]'
            line = re.sub(pattern, replace, line)
            
            # Create new variable declarations
            if replace not in new_display_vars:
                new_display_vars[replace] = replace +' = '+display_ref

        replaced_lines.append(' '*4*(indent_level+1)+line)
    
    lines = replaced_lines  # Substitue lines
    
    # Generate new display lines
    display_lines = []
    for v in new_display_vars:
        display_lines.append(' '*4*(indent_level+1)+new_display_vars[v])
    display_lines.append('')

    # Replace 'displays[]' with new variables and ident everything
    # lines = [' '*4*(indent_level+1)+n for i, n in enumerate(lines) if i not in display_matches_index]  # Pop display lines

    # Shuffle lines around in the right order
    lines[0:0] = display_lines  # Reinsert display lines up in the code
    top_func_args = '('+','.join(new_args)+')'
    lines = setup_lines+ ['def top_func'+top_func_args+':', ''] + lines + [' '*4*(indent_level+1)+'return '+func_name, '']

    new_code = '\n'.join(lines)

    return new_code


def zip_output(source, inner_inputs):
    """
        Finds the variables in the return statement, uses them to create a new output_tuple object and returns
        the newly created tuple
    """
    pass

def zip_input(source, inner_inputs):
    """
        Finds the variables in the signature of the function, replaces them with a tuple and unpicks the variables
        below
    """
    pass

def vectorize(source):
    pass