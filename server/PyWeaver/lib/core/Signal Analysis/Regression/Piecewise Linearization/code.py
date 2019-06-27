import ruptures as rpt
from scipy import interpolate

def f(x, y):
    pen = float(display['pen'])
    algo = rpt.Pelt(model="rbf").fit(y)
    breakpoint_index = algo.predict(pen=4)
    
    knots = []
    
    for b in breakpoint_index[:-1]:
        knots.append(b-1)
        knots.append(b)
        
    k = 1
    tck = interpolate.splrep(x, y, s=0, t=knots, task = -1, k=k)        
    ynew = interpolate.splev(x, tck, der=0)
    
    return ynew
    