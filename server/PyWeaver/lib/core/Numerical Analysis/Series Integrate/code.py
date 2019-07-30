from scipy import integrate

def f(x, y, y0=None):
    
    cte = float(display['cte'])
    
    if y0 is None:
        y0 = cte
    
    y_int = integrate.cumtrapz(y, x, initial=0)+y0
    
    return x, y_int