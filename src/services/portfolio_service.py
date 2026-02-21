from foliotrack.domain.Portfolio import Portfolio
from foliotrack.storage.PortfolioRepository import PortfolioRepository
from src.config import PORTFOLIOS_DIR


class PortfolioService:
    def __init__(self):
        self.repo = PortfolioRepository()

    def get_portfolio_files(self) -> list:
        """Get list of JSON files in Portfolios directory"""
        if not PORTFOLIOS_DIR.exists():
            PORTFOLIOS_DIR.mkdir(parents=True, exist_ok=True)
        return list(PORTFOLIOS_DIR.glob("*.json"))

    def get_portfolio_filenames(self) -> list:
        """Get list of JSON filenames in Portfolios directory"""
        files = self.get_portfolio_files()
        return [f.name for f in files]

    def load_portfolio(self, filename: str) -> Portfolio:
        """Load portfolio from JSON file"""
        # handling both full path and just filename
        filepath = PORTFOLIOS_DIR / filename

        try:
            return self.repo.load_from_json(str(filepath))
        except Exception as e:
            raise Exception(f"Error loading portfolio {filename}: {str(e)}")

    def save_portfolio(self, portfolio: Portfolio, filename: str) -> str:
        """Save portfolio to JSON file. Returns the full path."""
        try:
            # Ensure directory exists
            PORTFOLIOS_DIR.mkdir(parents=True, exist_ok=True)

            filepath = PORTFOLIOS_DIR / filename
            self.repo.save_to_json(portfolio, str(filepath))
            return str(filepath)
        except Exception as e:
            raise Exception(f"Error saving portfolio: {str(e)}")

    def buy_security(
        self,
        portfolio: Portfolio,
        ticker: str,
        volume: float,
        price: float,
        currency: str,
    ):
        portfolio.buy_security(
            ticker=ticker,
            volume=volume,
            price=price,
            currency=currency,
        )

    def sell_security(self, portfolio: Portfolio, ticker: str, volume: float):
        portfolio.sell_security(ticker=ticker, volume=volume)
