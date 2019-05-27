def f(x, y):
    if type(y) != list:
        y = [y]

    z = dict()

    z['uuid'] = '123'
    z['traces'] = []

    for s in y:
        trace = dict()
        trace['x'] = x.tolist()
        trace['y'] = s.tolist()
        trace['type'] = "scatter"
        z['traces'].append(trace)

    z['layout'] = {'width': 350, 'height': 350}

    return z