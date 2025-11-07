import os
import sys
from pathlib import Path
import pytest
from streamlit.testing.v1.app_test import AppTest

# Add the parent directory to sys.path to make imports work
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def original_dir():
    # Store original directory
    original = os.getcwd()
    # Change to the directory containing dashboard.py for proper path resolution
    os.chdir(str(Path(__file__).parent.parent))
    yield original
    # Restore the original directory after test
    os.chdir(original)


@pytest.mark.parametrize(
    "filename",
    [
        "pages/compare_securities.py",
        "pages/load_portfolio.py",
        "pages/equilibrium_buy.py",
    ],
)
def test_page_loads(original_dir, filename):
    # Initialize the app test with the main app
    at = AppTest.from_file("app.py").run()

    # Try to switch to the page
    at.switch_page(filename)
    at.run()

    # Check if there were any exceptions
    assert not at.exception, (
        f"Exception occurred while loading {filename}: {at.exception}"
    )
