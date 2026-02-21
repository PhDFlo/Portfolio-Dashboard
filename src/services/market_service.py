from foliotrack.services.MarketService import MarketService as FoliotrackMarketService
from foliotrack.domain.Portfolio import Portfolio
import yfinance as yf
import pandas as pd


class MarketService:
    def __init__(self):
        self.service = FoliotrackMarketService()

    def update_prices(self, portfolio: Portfolio):
        """Update prices for all securities in the portfolio"""
        self.service.update_prices(portfolio)

    def get_security_historical_data(
        self, tickers: list[str], start_date: str, interval="1d"
    ):
        """Fetch historical market data for all tickers using yfinance and forward fill missing data."""
        # Set pandas option to avoid future warnings
        pd.set_option("future.no_silent_downcasting", True)

        stock = yf.Tickers(tickers)
        hist = stock.history(start=start_date, period="max", interval=interval)
        # Fill missing data with values from previous dates
        hist.ffill(inplace=True)
        return hist
