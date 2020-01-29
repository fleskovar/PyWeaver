import numpy as np
import yfinance as yf

def f():
    ticker = display['ticker']
    start_date = display['start_date']
    end_date = display['end_date']
    
    data = yf.download(ticker, start_date, end_date) #returns a pandas
    return data