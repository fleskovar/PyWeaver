import numpy as np
import pandas as pd
import seaborn as sns
from io import StringIO
import base64

def f(data):
		
	if type(data) != list:
		data = [data]

	# For now it only accepts a list of (name, np.array)

	sns.set(style='ticks', color_codes='True')
	
	if len(data) > 1:
		z = pd.DataFrame()
		for d in data:
			z[d['name']] = d['data'].T
		# For more than one column, make a pair plot
		g = sns.pairplot(z)	
		fig = g.fig
	else:
		# For one column, make a histogram
		column = data[0]['data']		
		fig = sns.distplot(column).figure	
	
	my_stringIObytes = StringIO()
	fig.savefig(my_stringIObytes, format='jpg')
	my_stringIObytes.seek(0)
	img = base64.b64encode(my_stringIObytes.read())
	return img