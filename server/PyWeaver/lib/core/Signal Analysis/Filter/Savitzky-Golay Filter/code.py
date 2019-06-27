import numpy as np
from scipy.signal import savgol_filter

def f(i):
    win_length = int(display['win_length'])
    polyorder = int(display['polyorder'])
    
    if win_length % 2 == 0:
        # Forces the window length to be odd
        win_length = win_length + 1
    o = savgol_filter(i, win_length, polyorder)
    return o