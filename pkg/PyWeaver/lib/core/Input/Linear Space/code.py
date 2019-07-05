import numpy as np

def f():
    x0 = float(display['x0'])
    x1 = float(display['x1'])
    points = float(display['points'])
    x = np.linspace(x0, x1, points)
    return x