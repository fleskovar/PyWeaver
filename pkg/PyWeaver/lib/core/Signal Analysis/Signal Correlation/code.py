from scipy import signal
import  numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def f(x1, y1, x2, y2):
    
    l1 = len(x1)
    l2 = len(x2)
    l = l1 if l1 < l2 else l2
    
    corr = signal.correlate(y1, y2, mode='same') / l
    
    fig, (ax_orig, ax_noise, ax_corr) = plt.subplots(3, 1, sharex=True)
    ax_orig.plot(y1)
    ax_orig.set_title('Signal 1')
    ax_noise.plot(y2)
    ax_noise.set_title('Signal 2')
    ax_corr.plot(corr)
    ax_corr.set_title('Correlation')
    ax_orig.margins(0, 0.1)
    fig.tight_layout()
    
    figfile = BytesIO()
    fig.savefig(figfile, format='jpg')
    figfile.seek(0)
    img = base64.b64encode(figfile.getvalue())
    img = img.decode('utf8')
    
    return img