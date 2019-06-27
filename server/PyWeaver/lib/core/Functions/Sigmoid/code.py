import numpy as np

def f(x):
    loc = float(display['loc'])
    scale = float(display['scale'])
    y = 1.0 / (1 + np.exp(scale*(x-loc)))
    return y