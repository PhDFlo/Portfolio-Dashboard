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
    at = AppTest.from_file("app.py").run()

    # Switch to the load_portfolio page to render it within the full app
    at.switch_page(page_file)
    at.run()

    # There should be a selectbox for portfolio files
    assert at.selectbox, "No selectbox found on load_portfolio page"

    # Select default file (e.g. investment_example.json)
    at.selectbox(key="portfolio_file_select").set_value("investment_example.json").run()

    # Click on the "Load" button
    at.button(key="load").click().run()

    expected_df = pd.DataFrame(
        {
            "Name": [
                "Airbus SE",
                "NVIDIA Corporation",
                "LVMH Mo\u00ebt Hennessy - Louis Vuitton, Soci\u00e9t\u00e9 Europ\u00e9enne",
            ],
            "Ticker": ["AIR.PA", "NVDA", "MC.PA"],
            "Currency": ["EUR", "USD", "EUR"],
            "Price": [200.0, 150.0, 600.0],
            "Actual Share": [0.8441, 0.0349, 0.1211],
            "Target Share": [0.5, 0.2, 0.3],
            "Quantity": [20.0, 1.0, 1.0],
        }
    )

    for key in expected_df.keys():
        assert at.dataframe[0].value[key].equals(expected_df[key]), (
            f"Mismatch in column {key}"
        )


def test_update_security_price(page_file, original_dir):
    """Select a portfolio file and click Load (or Refresh)"""
    # Initialize the app test with the main app so pages and sidebar are registered
    at = AppTest.from_file("app.py").run()

    # Switch to the load_portfolio page to render it within the full app
    at.switch_page(page_file)
    at.run()

    # Select default file (e.g. investment_example.json)
    at.selectbox(key="portfolio_file_select").set_value("investment_example.json").run()

    # Click on the "Load" button
    at.button(key="load").click().run()

    # Click on the "Update Securities Price" button
    at.button(key="update_securities_price").click().run()

    # Check that prices have been updated (not equal to initial values)
    updated_prices = at.dataframe[0].value["Price"]
    initial_prices = [500.0, 300.0, 200.0]
    assert not updated_prices.equals(pd.Series(initial_prices)), (
        "Prices were not updated"
    )


def test_save_file(page_file, original_dir):
    """Select a portfolio file, load it, modify it and save it"""
    # Creates save file as selectox options must exist in Apptest
    filepath = "./Portfolios/investment_test.json"
    with open(filepath, "w"):
        pass

    # Initialize the app test with the main app so pages and sidebar are registered
    at = AppTest.from_file("app.py").run()

    # Switch to the load_portfolio page to render it within the full app
    at.switch_page(page_file)
    at.run()

    # Select default file (e.g. investment_example.json)
    at.selectbox(key="portfolio_file_select").set_value("investment_example.json").run()

    # Click on the "Load" button
    at.button(key="load").click().run()

    # Modify the save filename
    at.selectbox(key="portfolio_file_save").set_value("investment_test.json").run()

    # Click on the "Save" button
    at.button(key="save_button").click().run()

    assert os.path.exists(filepath), "Saved file does not exist"

    # Clean up
    os.remove(filepath)
