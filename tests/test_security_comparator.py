import os
import sys
import unittest
from pathlib import Path
import pytest

from streamlit.testing.v1.app_test import AppTest

# Add the parent directory to sys.path to make imports work
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestSecurityComparator(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.page_file = "pages/compare_securities.py"

    def setUp(self):
        # Change to the directory containing dashboard.py for proper path resolution
        self.original_dir = os.getcwd()
        os.chdir(str(Path(__file__).parent.parent))

    def tearDown(self):
        # Restore the original directory
        os.chdir(self.original_dir)

    def test_increment_and_add(self):
        """A user increments the number input, then clicks Add"""
        at = AppTest.from_file(self.page_file).run()

        # Initial A
        for i in range(12):
            at.number_input[i].increment().run()
            print(at.number_input[i].value)

        # Better assertion to be found
        assert at.number_input[0].value == pytest.approx(10000.01, 0.001)
        assert at.number_input[1].value == pytest.approx(0.07, 0.001)
        assert at.number_input[2].value == pytest.approx(0.01, 0.001)
        assert at.number_input[3].value == pytest.approx(0.015, 0.001)
        assert at.number_input[4].value == pytest.approx(0.015, 0.001)
        assert at.number_input[5].value == pytest.approx(0.182, 0.001)
        assert at.number_input[6].value == pytest.approx(10000.01, 0.001)
        assert at.number_input[7].value == pytest.approx(0.09, 0.001)
        assert at.number_input[8].value == pytest.approx(0.01, 0.001)
        assert at.number_input[9].value == pytest.approx(0.015, 0.001)
        assert at.number_input[10].value == pytest.approx(0.015, 0.001)
        assert at.number_input[11].value == pytest.approx(0.31, 0.001)

    def test_run_comparison(self):
        """Run security comparison after incrementing number input"""
        at = AppTest.from_file(self.page_file).run()
        at.number_input[0].increment().run()
        at.button[0].click().run()
        # Bettter assertion to be found
        assert at.button[0].value is True
