from streamlit.testing.v1 import AppTest
import sys
from pathlib import Path


def test_increment_and_add():
    """A user increments the number input, then clicks Add"""
    sys.path.insert(0, str(Path(__file__).parent.parent))
    at = AppTest.from_file("pages/compare_securities.py").run()
    at.number_input[0].increment().run()
    print(at.number_input[0].value)

    at.button[0].click().run()
    assert at.markdown[0].value == "Beans counted: 1"
