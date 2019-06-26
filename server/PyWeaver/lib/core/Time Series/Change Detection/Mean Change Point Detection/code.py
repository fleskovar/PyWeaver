import ruptures as rpt

def f(x, y):
    pen = float(display['pen'])
    algo = rpt.Pelt(model="rbf").fit(y)
    breakpoint_index = algo.predict(pen=10)
    
    breakpoints = []
    
    for b in breakpoint_index[:-1]:
        breakpoints.append(b-1)
        breakpoints.append(b)
    
    return breakpoint_index, breakpoints
    