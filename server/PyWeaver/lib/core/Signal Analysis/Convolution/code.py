import numpy as np

def f(x, y, g):
    conv_type = display['conv_type']
    fg = np.convolve(g/g.sum(), y, mode=conv_type)
    xn = x
    yn = fg
    
    len_fg = len(fg)
    len_x = len(fg)
    
    if len_fg > len_x:
        diff_len = len_fg - len_x
        diff_len = int(diff_len / 2)
        yn = fg[diff_len:-diff_len]
    elif len_x > len_fg:
        diff_len = len_x - len_fg
        diff_len = int(diff_len / 2)
        xn = x[diff_len:-diff_len]
    
    return xn, yn