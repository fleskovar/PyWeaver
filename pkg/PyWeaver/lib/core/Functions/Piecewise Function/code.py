import numpy as np

def f(x):
    conds = [
        x < 0,
        (x >= 0.3) & (x < 0.6),
        x>=0.6
    ]
    
    funcs = [
        lambda x: x,
        lambda x: 2,
        lambda x: x**2
    ]
    
    
    
    y = np.piecewise(x, conds, funcs)
    return y