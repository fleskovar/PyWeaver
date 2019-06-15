import numpy as np

def f(x):
	if display['custom_bins']:
		bins = int(display['bins'])
		h, e = np.histogram(x, bins, density=True)
	else:
		h, e = np.histogram(x, density=True)
	
	chart = dict()
	chart['uuid'] = '123'
	chart['traces'] = []
	
	trace = dict()
	trace['x'] = e.tolist()
	trace['y'] = h.tolist()
	trace['type'] = "bar"	
	
	chart['traces'].append(trace)	
	chart['layout'] = {'width': 350, 'height': 350}
	
	return h, e, chart