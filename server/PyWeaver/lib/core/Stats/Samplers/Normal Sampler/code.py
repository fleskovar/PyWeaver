import numpy as np

def f(mu=None, sd =None, size=None):
    
    mu = float(display['mu']) if mu is None else mu
    sd = float(display['sd']) if sd is None else sd
    size = int(display['size']) if size is None else size
    
    samples = np.random.normal(mu, sd, size)
    return samples