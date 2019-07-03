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
	
	no_name_series = 0
	
	if len(data) > 1:
		z = pd.DataFrame()
		data_names = list(map(lambda x: x.strip(), inputs['data']))
		
		for i, d in enumerate(data):
			
			# Checks if a name was given to the series
			if len(data_names[i]) == 0:
				# If no name was provided to the connection, make up one
				data_name = 'input_'+str(no_name_series)
				no_name_series = no_name_series + 1
			else:
				# If a name was provided to the connection, use it
				data_name = data_names[i]

			z[data_name] = d.T
		# For more than one column, make a pair plot
		g = sns.pairplot(z)	
		fig = g.fig
	else:
		# For one column, make a histogram
		column = data
		data_name = data_names[0] if len(data_names[0]) > 0 else 'Input Data'
		fig = sns.distplot(column).figure	
	
	my_stringIObytes = StringIO()
	fig.savefig(my_stringIObytes, format='jpg')
	my_stringIObytes.seek(0)
	img = base64.b64encode(my_stringIObytes.read())
	return img