import numpy as np

def f(x):
    y = np.piecewise(x, [x < 0.5, x >= 0.5], [-1, 1])
    return y