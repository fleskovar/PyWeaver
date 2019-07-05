import numpy as np
def f():
	
	v = display['grid_data']['data']
	v = v[:-1]  #Get rid of trailing empty row
	v = np.array(v).flatten()
	v = v.astype('float64')

	return v