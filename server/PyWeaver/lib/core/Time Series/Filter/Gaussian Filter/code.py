import numpy as np
from scipy.ndimage import gaussian_filter1d

def f(i):
    sigma = float(display['sigma'])
    max_sigma = int(display['max_sigma'])
    o = gaussian_filter1d(i, sigma, truncate=max_sigma)
    return o