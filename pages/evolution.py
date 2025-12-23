import streamlit as st
import pandas as pd
from datetime import datetime
from dashboard import (
    side_bar_file_operations,
)
from foliotrack.Portfolio import Portfolio
from dashboard.utils_evolution import (
    get_security_historical_data,
    plot_pie_chart,
    plot_portfolio_evolution,
)


# Side bar for file operations
side_bar_file_operations()

min_y_exchange = st.sidebar.number_input(
    "Min value for buy/sold (plotting)",
    value=-5,
)

max_y_exchange = st.sidebar.number_input(
    "Max value for buy/sold (plotting)",
    value=20,
)

# Display current portfolio in editable table
if "portfolio" not in st.session_state:
    # Ensure a portfolio object exists in session state for pages run standalone
    st.session_state.portfolio = Portfolio()

ticker_list = [ticker for ticker in st.session_state.portfolio.securities]

col1, col2 = st.columns([3, 1])

# If there is at least one ticker
if ticker_list != []:
    # Display portfolio value evolution over time
    with col1:
        start_date = min(event["date"] for event in st.session_state.portfolio.history)

        # Get historical data for all tickers in portfolio
        hist_tickers = get_security_historical_data(
            ticker_list, start_date=start_date, interval="1d"
        )

        plot_portfolio_evolution(
            portfolio=st.session_state.portfolio,
            ticker_list=ticker_list,
            hist_tickers=hist_tickers,
            Date=pd.DatetimeIndex(hist_tickers.index),
            min_y_exchange=min_y_exchange,
            max_y_exchange=max_y_exchange,
        )

    # Display target vs actual shares in donut charts
    with col2:
        plot_pie_chart(portfolio=st.session_state.portfolio, ticker_list=ticker_list)
