import scipy.fftpack
import numpy as np

def f(x, y):
    
    N = len(y)
    T = 1.0 / (x[1]-x[0])
    yf = scipy.fftpack.rfft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

    chart = dict()
    chart['uuid'] = '123'
    chart['traces'] = []

    trace = dict()
    trace['x'] = xf.tolist()
    trace['y'] = yf.tolist()
    trace['type'] = "bar"	
    
    chart['traces'].append(trace)	
    chart['layout'] = {'width': 380, 'height': 450}

    return xf, yf, chart