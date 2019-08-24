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

    # Save the position of all the lines of code above the first function
    setup_lines = lines[0:def_matches_index[0]-1]
    setup_lines.append('')
    lines = lines[def_matches_index[0]:]

    # Just in case, save the indentation level of the fisrt function (should be 0)
    indent_level = len(lines[def_matches_index[0]].split(' '*4))

    # Find all lines of code that use the 'display' dictionary
    display_rgx = r".*=.*display\[.*"
    display_matches = list(map(lambda l: bool(re.match(display_rgx, l)), lines))
    display_matches_index = [i for i, m in enumerate(display_matches) if m]

    display_lines = [' '*4*(indent_level-1)+n.strip() for i, n in enumerate(lines) if i in display_matches_index]  # Extract lines 
    display_lines.append('')
    lines = [' '*4*(indent_level-1)+n for i, n in enumerate(lines) if i not in display_matches_index]  # Pop display lines

    # Shuffle lines around in the right order
    lines[0:0] = display_lines  # Reinsert display lines up in the code
    top_func_args = '('+','.join(new_args)+')'
    lines = setup_lines+ ['def top_func'+top_func_args+':', ''] + lines + [' '*4*(indent_level-1)+'return '+func_name, '']

    new_code = '\n'.join(lines)

    return new_code

def vectorize(source):
    pass