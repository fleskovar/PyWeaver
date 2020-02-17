def f(x):
	
	if type(x) != list:
		x = [x]

	x2 = []

	# If there are lists inside the list, unpack them
	for t in x:
		if type(t) is list:
			for tt in t:
				x2.append(tt)
		else:
			x2.append(t)
	x = x2

	chart = dict()
	chart['uuid'] = '123'
	chart['traces'] = x
	
	chart['layout'] = {	'width': 350,
                       	'height': 350,
                      	'yaxis2': {
    						'overlaying': 'y',
    						'side': 'right'
						}
                      }
	
	return chart