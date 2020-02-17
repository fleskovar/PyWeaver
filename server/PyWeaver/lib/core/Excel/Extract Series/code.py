import numpy as np
from datetime import datetime

def f(table, epoch=None):
    column_name = display['column_name']
    
    if epoch is None:
        epoch_str = display['epoch_str']
        epoch = datetime.strptime(epoch_str, "%d/%m/%Y")

    y = table[column_name].values
    x = np.array(list(map(lambda x: x.total_seconds(), table[column_name].index - epoch)))
    
    return x, y