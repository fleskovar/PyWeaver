import context
from PyWeaver.code_parsing import parse_function

def test():
    return 1

def test_answer():
    assert test() == 1

if __name__ == '__main__':
    
    f = open(r'C:\Projects\PyWeaver\server\test\res\test_1.py')
    code = f.read()

    success, func_name, input_vars, input_vars_dict, output_vars = parse_function(code)