import numpy as np
from scipy.signal import ricker, gaussian, barthann, flattop, cosine, triang

def f():
    window_type = display['window_type']
    window_size = int(display['size'])
    p = float(display['param'])
    
    window = np.zeros(window_size)
    
    if window_type == 'square':
        window = np.ones(window_size)
    elif window_type == 'exponential':
        window = np.exp(np.arange(window_size)*p)
    elif window_type == 'hanning':
        window = np.hanning(window_size)
    elif window_type == 'blackman':
    	window = np.blackman(window_size)
    elif window_type == 'ricker':
        window = ricker(window_size, p)
    elif window_type == 'gaussian':
        window = gaussian(window_size, p)
    elif window_type == 'barthann':
        window = barthann(window_size)
    elif window_type == 'flattop':
        window = flattop(window_size)
    elif window_type == 'cosine':
        window = cosine(window_size)
    elif window_type == 'triangle':
        window = triang(window_size)
    
    return window