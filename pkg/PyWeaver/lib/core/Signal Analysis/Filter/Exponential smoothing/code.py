import numpy as np

def f(i):
    alpha = float(display['alpha'])
    
    o = np.zeros(len(i))
    o[0] = o[0]
    
    for j, s in enumerate(i[1:]):
        o[j+1] = alpha * i[j+1] + (1-alpha) * o[j]
    
    return o