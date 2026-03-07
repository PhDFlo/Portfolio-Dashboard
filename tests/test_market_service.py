import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.market_service import MarketService

def test_market_service_update_prices():
    """Verify that MarketService shim calls foliotrack backend."""
    with patch('src.services.market_service.FoliotrackMarketService') as MockBackend:
        mock_instance = MockBackend.return_value
        service = MarketService()
        portfolio = MagicMock()
        
        service.update_prices(portfolio)
        mock_instance.update_prices.assert_called_once_with(portfolio)

def test_market_service_historical_data():
    """Verify that MarketService shim calls historical data method."""
    with patch('src.services.market_service.FoliotrackMarketService') as MockBackend:
        mock_instance = MockBackend.return_value
        service = MarketService()
        
        service.get_security_historical_data(["AAPL"], "2023-01-01")
        mock_instance.get_historical_data.assert_called_once_with(["AAPL"], "2023-01-01", None)
