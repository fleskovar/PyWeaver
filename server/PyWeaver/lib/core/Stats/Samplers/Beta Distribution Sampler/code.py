import numpy as np

def f(alpha=None, beta =None, size=None):
    
    alpha = float(display['alpha']) if alpha is None else alpha
    beta = float(display['beta']) if beta is None else beta
    
    size = int(display['size']) if size is None else size
    
    samples = np.random.beta(alpha, beta, size)
    
    return samples