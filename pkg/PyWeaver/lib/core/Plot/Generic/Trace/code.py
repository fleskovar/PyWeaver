def f(x, y):
	
	trace = dict()
	trace['x'] = x.tolist()
	trace['y'] = y.tolist()
	trace['name'] = display['trace_name']
	trace['type'] = display['trace_type']	

	if display['trace_type'] == 'scatter':
		trace['mode'] = 'markers'	
	
	return trace