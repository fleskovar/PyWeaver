from scipy.stats import norm
import numpy as np

def f():
    
    sd = float(display['sd'])
    mu = float(display['mu'])
    points = float(display['points'])

    domain_start = float(display['domain_start'])
    domain_end = float(display['domain_end'])

    x = np.linspace(domain_start, domain_end, points)
    y = norm.pdf(x, mu, sd)    

    return x, y