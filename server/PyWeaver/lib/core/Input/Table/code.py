import numpy as np
import pandas as pd


def f():

    x = display['grid_data']['data']
    cols = display['grid_data']['columns']
    x = x[:-1]  # Get rid of the empty bottom row
    df = pd.DataFrame(x, columns=cols)

    col_types = display['grid_data']['column_types']

    for i, t in enumerate(col_types):
        c = cols[i]  # Column name

        if t == 'Number':
            df[c] = pd.to_numeric(df[c])
        elif t == 'Date':
            df[c] = pd.to_datetime(df[c])
        else:
            # Default: convert to text
            df[c] = pd.to_string(df[c])
        
    return df