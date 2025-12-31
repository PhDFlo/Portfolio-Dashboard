import streamlit as st
import pandas as pd
from foliotrack.domain.Portfolio import Portfolio
from dashboard import (
    side_bar_file_operations,
    table_section,
)

# Side bar for file operations
st.session_state.file_list = side_bar_file_operations()

# Display current portfolio in editable table
if "portfolio" not in st.session_state:
    # Ensure a portfolio object exists in session state for pages run standalone
    st.session_state.portfolio = Portfolio()

# List of tickers
ticker_list = [ticker for ticker in st.session_state.portfolio.securities]

# List of tickers for buy and sell
st.session_state.ticker_options = [""] + ticker_list

st.subheader("Security List")
table_section(st.session_state.ticker_options, st.session_state.file_list)
