import numpy as np

def f(min_val=None, max_val =None, size=None):
    
    min_val = float(display['min_val']) if min_val is None else min_val
    max_val = float(display['max_val']) if max_val is None else max_val
    size = int(display['size']) if size is None else size
    
    samples = np.random.uniform(min_val, max_val, size)
    
    return samples