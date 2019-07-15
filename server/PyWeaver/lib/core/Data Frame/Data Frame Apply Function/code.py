import numpy as np

def f(df, func, new_name='new_col'):
    
    var_table = display['grid_data']['data']
    var_table = var_table[:-1]  #Get rid of trailing empty row

    # G is a dummy function that maps the variable names from the table
    # and then applies 'func' to the row of a table
    def g(dataframe_row):
        input_dict = dict()
        
        for table_row in var_table:
            var_name = table_row[0]
            
            # Look for semicolon separated strings
            col_names = list(filter(None, table_row[1].split(';')))
            
            if len(col_names) == 1:
                # If only one name is used, only append one value
                input_dict[var_name] = dataframe_row[col_names[0].strip()]
            else:
                # Semicolon separated names are aggregated into a list
                vals = []
                for c_name in col_names:
                    vals.append(dataframe_row[c_name.strip()])
                # Input values as a numpy array (could be changed to a list)
                input_dict[var_name] = np.array(vals)
            
        row_result = func(**input_dict)
        return row_result
    
    # Apply dummy function g to every row
    df[new_name] = df.apply(lambda row: g(row), axis=1)
    
    return df