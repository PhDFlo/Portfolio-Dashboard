import os
import sys
import unittest
from pathlib import Path

from streamlit.testing.v1.app_test import AppTest

# Add the parent directory to sys.path to make imports work
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestMultiPageApp(unittest.TestCase):
    def setUp(self):
        # Change to the directory containing dashboard.py for proper path resolution
        self.original_dir = os.getcwd()
        os.chdir(str(Path(__file__).parent.parent))

    def tearDown(self):
        # Restore the original directory
        os.chdir(self.original_dir)

    def test_all_pages_load(self):
        # List of pages to test
        pages = [
            "pages/compare_securities.py",
            "pages/load_portfolio.py",
            "pages/equilibrium_buy.py",
        ]

        for filename in pages:
            with self.subTest(filename=filename):
                # Initialize the app test with the main app
                at = AppTest.from_file("dashboard.py").run()

                # Try to switch to the page
                at.switch_page(filename)
                at.run()

                # Check if there were any exceptions
                self.assertFalse(
                    at.exception,
                    f"Exception occurred while loading {filename}: {at.exception}",
                )


# if __name__ == "__main__":
#    unittest.main()
