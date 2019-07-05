import numpy as np
import pandas as pd
from io import BytesIO
import base64
import matplotlib.pyplot as plt

def f(x, y):
    fig = plt.figure()
    plt.plot(x, y)        
    figfile = BytesIO()
    fig.savefig(figfile, format='jpg')
    figfile.seek(0)
    img = base64.b64encode(figfile.getvalue())
    img = img.decode('utf8')
    return img