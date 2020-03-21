import numpy as np
import yfinance as yf

def f():
    ticker = display['ticker']
    start_date = display['start_date']
    end_date = display['end_date']
    
    data = yf.download(ticker, start_date, end_date) #returns a pandas
    
    close_val = data['Close'].values
    open_val = data['Open'].values
    low_val = data['Low'].values
    high_val = data['High'].values
    
    dates = data['Close'].index.values
    
    return dates, close_val, high_val, low_val, open_val