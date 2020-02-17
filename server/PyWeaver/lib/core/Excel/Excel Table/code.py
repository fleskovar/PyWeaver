import numpy as np
import xlwings as xw
import pandas as pd

def f():
    file_path = display['file_path']
    sheet_name = display['sheet_name']
    cell_name = display['cell_name']

    wb = xw.Book(file_path)
    sht = wb.sheets[sheet_name]
    table = sht.range(cell_name).options(pd.DataFrame, expand='table').value

    return table