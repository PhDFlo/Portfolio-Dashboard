from foliotrack.services.MarketService import MarketService as FoliotrackMarketService
from foliotrack.domain.Portfolio import Portfolio


class MarketService:
    def __init__(self):
        self.service = FoliotrackMarketService()

    def update_prices(self, portfolio: Portfolio):
        """Update prices for all securities in the portfolio"""
        self.service.update_prices(portfolio)

    def get_security_historical_data(
        self, tickers: list[str], start_date: str, end_date: str = None
    ):
        """Fetch historical market data for all tickers using foliotrack's MarketService."""
        return self.service.get_historical_data(tickers, start_date, end_date)
