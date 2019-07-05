import numpy as np

def f(x, y):
    d = int(display['degree'])
    coeffs = np.polyfit(x, y, d)
    polynomial = np.poly1d(coeffs)
    y_p = polynomial(x)
    return coeffs, polynomial, y_p