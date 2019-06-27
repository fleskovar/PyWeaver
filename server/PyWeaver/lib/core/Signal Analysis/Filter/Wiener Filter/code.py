import numpy as np
from scipy.signal import wiener

def f(i):
    window = int(display['window'])
    
    use_power = display['use_power']
    
    if use_power:
        noise_power = float(display['power'])
    else:
        noise_power=None
        
    o = wiener(i, window, noise_power)
    return o