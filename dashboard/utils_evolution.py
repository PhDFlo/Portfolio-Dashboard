import yfinance as yf


def get_historical_data(tickers: list[str], start_date: str, interval="1d"):
    """Fetch historical market data for all tickers using yfinance"""
    stock = yf.Tickers(tickers)

    hist = stock.history(start=start_date, period="max", interval=interval)
    return hist
