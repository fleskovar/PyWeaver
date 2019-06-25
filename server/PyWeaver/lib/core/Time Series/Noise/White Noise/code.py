import numpy as np

def f(signal):
    sd = float(display['sd'])
    out = signal + np.random.normal(0, sd, len(signal))
    return out