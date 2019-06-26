import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def f(x, y):
	print(x)
	print(y)
	if type(y) is not list:
		y = [y]	
	
	fig, ax = plt.subplots()

	for d in y:
		ax.plot(x, d)
    
	my_stringIObytes = BytesIO()
	fig.savefig(my_stringIObytes, format='jpg')
	my_stringIObytes.seek(0)
	img = base64.b64encode(my_stringIObytes.read())
	return img