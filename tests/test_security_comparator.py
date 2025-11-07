import os
import sys
from pathlib import Path
import pytest
from streamlit.testing.v1.app_test import AppTest

# Add the parent directory to sys.path to make imports work
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def page_file():
    return "pages/compare_securities.py"


@pytest.fixture
def original_dir():
    # Store original directory
    original = os.getcwd()
    # Change to the directory containing app.py for proper path resolution
    os.chdir(str(Path(__file__).parent.parent))
    yield original
    # Restore the original directory after test
    os.chdir(original)


def test_edit_contracts(page_file, original_dir):
    """A user increments the number input, then clicks Add"""
    at = AppTest.from_file(page_file).run()

    # Initial A
    for i in range(12):
        at.number_input[i].increment().run()

    # Test assertions
    expected_values = [
        10000.01,
        0.07,
        0.01,
        0.015,
        0.015,
        0.182,
        10000.01,
        0.09,
        0.01,
        0.015,
        0.015,
        0.31,
    ]

    for i, expected in enumerate(expected_values):
        assert at.number_input[i].value == pytest.approx(expected, 0.001)


def test_run_comparison(page_file, original_dir):
    """Run security comparison after incrementing number input"""
    at = AppTest.from_file(page_file).run()
    at.number_input[0].increment().run()
    at.button[0].click().run()

    # Test assertions
    expected_values = [
        "Final value of PEA (pre-withdrawal): 42516.87 €",
        "Final value of PEA (after-tax): 36923.97 €",
        "Final value of CTO (pre-withdrawal): 74489.92 €",
        "Final value of CTO (after-tax): 55142.94 €",
    ]

    assert at.button[0].value is True
    for i, expected in enumerate(expected_values):
        assert at.markdown[i].value == expected_values[i]
