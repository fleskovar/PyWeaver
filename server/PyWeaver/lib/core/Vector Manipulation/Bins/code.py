import numpy as np

def f(vector, bins=None):
	
	if bins is None:
		min_v = np.min(vector)
		max_v = np.max(vector)
		bins = np.array([min_v, max_v])
	
	v = np.digitize(vector, bins)
	return v