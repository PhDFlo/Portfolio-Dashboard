import pytest
from unittest.mock import MagicMock
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Patch foliotrack if it's broken
try:
    import foliotrack.utils.Currency as CurrencyModule
    import foliotrack.domain.Security as SecurityModule
    import foliotrack.domain.Portfolio as PortfolioModule

    # Mock get_symbol to avoid FileNotFoundError
    def mock_get_symbol(code):
        symbols = {"EUR": "€", "USD": "$"}
        return symbols.get(code, code)

    # Patch the function where it is defined
    CurrencyModule.get_symbol = mock_get_symbol

    # Patch the function where it is imported
    SecurityModule.get_symbol = mock_get_symbol
    # Check if Portfolio uses it
    if hasattr(PortfolioModule, "get_symbol"):
        PortfolioModule.get_symbol = mock_get_symbol

except ImportError:
    pass
