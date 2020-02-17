import numpy as np

def f(x, y, breakpoints):
    i = 0

    segments = []

    for b in breakpoints:
        segments.append([
            x[i:b],
            y[i:b]
        ])
        i = b + 1

    return segments