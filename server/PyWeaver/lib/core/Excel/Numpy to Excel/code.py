import xlwings as xl

def f(x):
    wb_path = display['path']
    sheet_name = display['sheet']
    cell_name = display['cell']
    wb = xl.Book(wb_path)
    sh = wb.sheets(sheet_name)
    sh.range(cell_name).value = x