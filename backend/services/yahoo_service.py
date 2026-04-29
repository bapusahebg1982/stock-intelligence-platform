import yfinance as yf

def get_stock(ticker):
    return yf.Ticker(ticker)