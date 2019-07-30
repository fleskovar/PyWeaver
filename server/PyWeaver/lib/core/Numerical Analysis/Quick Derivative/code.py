import numpy as np

def f(x, y):
    dy = np.gradient(y, x)
    return x, dy