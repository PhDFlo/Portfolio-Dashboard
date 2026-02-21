import streamlit as st
from foliotrack.domain.Portfolio import Portfolio
from src.ui.components.sidebar import render_sidebar
from src.ui.fragments.portfolio_table import render_portfolio_table
from src.ui.fragments.portfolio_actions import render_portfolio_actions

# Ensure session state
if "portfolio" not in st.session_state:
    st.session_state.portfolio = Portfolio()

# Side bar for file operations
file_list = render_sidebar()

# List of tickers
ticker_list = [ticker for ticker in st.session_state.portfolio.securities]
# List of tickers for buy and sell
ticker_options = [""] + ticker_list

st.subheader("Security List")

# Render Table Fragment
render_portfolio_table()

# Render Actions Fragment
render_portfolio_actions(ticker_options, file_list)
