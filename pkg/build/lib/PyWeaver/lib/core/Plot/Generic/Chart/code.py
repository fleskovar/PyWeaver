def f(x):
	
	if type(x) != list:
		x = [x]
	
	chart = dict()
	chart['uuid'] = '123'
	chart['traces'] = x
	
	chart['layout'] = {'width': 350, 'height': 350}
	
	return chart