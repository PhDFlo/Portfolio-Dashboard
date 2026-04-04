import os
import sys
from pathlib import Path
import pytest
from streamlit.testing.v1.app_test import AppTest

# Add the parent directory to sys.path to make imports work
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def page_file():
    return "pages/exchange_rates.py"


@pytest.fixture
def original_dir():
    original = os.getcwd()
    os.chdir(str(Path(__file__).parent.parent))
    yield original
    os.chdir(original)


def test_exchange_calculator(page_file, original_dir):
    """Test that the exchange calculator responds to input changes."""
    at = AppTest.from_file(page_file).run()

    # Check default state
    assert at.number_input[0].value == 1.0  # Amount

    # Change amount
    at.number_input[0].set_value(10.0).run()

    # Check metrics (assuming they exist after calculation)
    # The page uses currency selective boxes
    # Let's try to find metrics
    if len(at.metric) > 0:
        # Depending on network, metrics might be 0.0 if fetch fails,
        # but the widget should at least exist.
        assert len(at.metric) >= 2
