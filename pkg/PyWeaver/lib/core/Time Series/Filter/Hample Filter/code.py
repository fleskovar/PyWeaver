import numpy as np
import pandas as pd

def hampel(vals):
	k = int(display['k'])
	t0 = int(display['t0'])
	
	s = pd.Series(vals)
	
	L= 1.4826
	rolling_median=s.rolling(k).median()
	difference=np.abs(rolling_median-s)
	median_abs_deviation=difference.rolling(k).median()
	threshold= t0 *L * median_abs_deviation
	outlier_idx=difference>threshold
	s[outlier_idx]=rolling_median[outlier_idx]
	
	filtered = s.as_matrix().flatten()
		
	return filtered
