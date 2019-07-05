import numpy as np
from scipy import interpolate

def f(x, y, knots=None):
    k = int(display['k'])
    if knots is None:
    	tck = interpolate.splrep(x, y, s=0, k=k)
    else:
        tck = interpolate.splrep(x, y, s=0, t=knots, task = -1, k=k)
        
    ynew = interpolate.splev(x, tck, der=0)
    return ynew