import numpy as np
def f():
	
	export_with_name = display['export_name']
	
	x = display['grid_data']
	x = x[:-1]
	x = np.array(x)
	x = x.astype('float64')

	return_val = x

	if export_with_name == True:
		col_name = display['col_name']
		return_val = dict(name= col_name, data= x)

	return return_val