import os
import pandas as pd
from pathlib import Path
import pytest
from streamlit.testing.v1.app_test import AppTest

# Add parent directory to sys.path is done in other tests by changing cwd


@pytest.fixture
def page_file():
    return "pages/load_portfolio.py"


@pytest.fixture
def original_dir():
    original = os.getcwd()
    os.chdir(str(Path(__file__).parent.parent))
    yield original
    os.chdir(original)


def test_select_and_load_file(page_file, original_dir):
    """Select a portfolio file and click Load (or Refresh)"""
    # Initialize the app test with the main app so pages and sidebar are registered
    at = AppTest.from_file("dashboard.py").run()

    # Switch to the load_portfolio page to render it within the full app
    at.switch_page(page_file)
    at.run()

    # There should be a selectbox for portfolio files
    assert at.selectbox, "No selectbox found on load_portfolio page"

    # Select default file (e.g. investment_example.json)
    at.selectbox(key="portfolio_file_select").set_value("investment_example.json").run()

    # CLick on the "Load" button
    if at.button:
        at.button(key="load").click().run()

    expected_df = pd.DataFrame(
        {
            "Name": [
                "Amundi MSCI World UCITS Security",
                "NVIDIA Corporation",
                "iShares Core MSCI Emerging Markets IMI UCITS Security",
            ],
            "Ticker": ["AMDW", "NVDA", "EIMI.L"],
            "Currency": ["EUR", "USD", "EUR"],
            "Price": [500.0, 300.0, 200.0],
            "Actual Share": [0.92, 0.03, 0.06],
            "Target Share": [0.5, 0.2, 0.3],
            # "Amount Invested (€)": [10000.0, 255.63, 600.0], # Amount invested not tested as currency change will affect the result
            "Number Held": [20.0, 1.0, 3.0],
        }
    )

    for key in expected_df.keys():
        assert at.dataframe[0].value[key].equals(expected_df[key]), (
            f"Mismatch in column {key}"
        )
