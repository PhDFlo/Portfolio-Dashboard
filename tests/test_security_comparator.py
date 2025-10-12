import os
import sys
import unittest
from pathlib import Path

from streamlit.testing.v1.app_test import AppTest

# Add the parent directory to sys.path to make imports work
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestMultiPageApp(unittest.TestCase):
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
        at.number_input[0].increment().run()
        at.button[0].click().run()
        # Bettter assertion to be found
        assert at.button[0].value is True
