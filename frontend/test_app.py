"""test_demo.py"""
from streamlit.testing.v1 import AppTest

def test_chat():
    """A user increments the number input, then clicks Add"""
    at = AppTest.from_file("app.py").run()
    # at.number_input[0].increment().run()
    # at.button[0].click().run()
    # at.chat_message("assistant",avatar="🤖").write()
    # assert at.chat_message()