import numpy as np
from scipy.stats import norm

def f(x):
	mu, std = norm.fit(x)	
	return mu, std
	