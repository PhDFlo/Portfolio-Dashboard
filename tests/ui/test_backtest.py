import os
import sys
from pathlib import Path
import pytest
from streamlit.testing.v1.app_test import AppTest

# Add the parent directory to sys.path to make imports work
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


@pytest.fixture
def page_file():
    return "pages/backtest.py"


@pytest.fixture
def original_dir():
    original = os.getcwd()
    os.chdir(str(Path(__file__).parent.parent.parent))
    yield original
    os.chdir(original)


def test_backtest_load(page_file, original_dir):
    """Test that the backtest page loads and has settings."""
    from foliotrack.domain.Portfolio import Portfolio

    at = AppTest.from_file(page_file)
    at.session_state["portfolio"] = Portfolio()
    at.run()

    # Check for date inputs (Start Date, End Date)
    assert len(at.date_input) >= 2

    # Check for Simulation button (it's inside render_backtest_view)
    # The backtest_view fragment should render if portfolio is in session_state.
    # Let's check for buttons
    assert len(at.button) >= 1
