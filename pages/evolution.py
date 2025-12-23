import streamlit as st
import pandas as pd
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

# Sidebar input
start_date = st.sidebar.date_input(
    "Start Date (plotting)",
    format="YYYY-MM-DD",
    value=pd.to_datetime("2023-01-01"),
)

end_date = st.sidebar.date_input(
    "End Date (plotting)",
    format="YYYY-MM-DD",
    value=pd.to_datetime("today"),
)

# Display current portfolio in editable table
if "portfolio" not in st.session_state:
    # Ensure a portfolio object exists in session state for pages run standalone
    st.session_state.portfolio = Portfolio()

ticker_list = [ticker for ticker in st.session_state.portfolio.securities]

col1, col2 = st.columns([3, 1])

# Display portfolio value evolution over time
with col1:
    if ticker_list != []:
        # Find the earliest date in portfolio history
        earliest_date = min(
            event["date"] for event in st.session_state.portfolio.history
        )

        from datetime import datetime

        # Adjust earliest date if it's before the selected start date
        if datetime.strptime(earliest_date, "%Y-%m-%d").date() > start_date:
            earliest_date = start_date

        print(earliest_date)
        # Get historical data for all tickers in portfolio
        hist_tickers = get_security_historical_data(
            ticker_list, start_date=earliest_date, interval="1d"
        )

        plot_portfolio_evolution(
            portfolio=st.session_state.portfolio,
            ticker_list=ticker_list,
            hist_tickers=hist_tickers,
            Date=pd.DatetimeIndex(hist_tickers.index),
            start_date=start_date,
            end_date=end_date,
        )

# Display target vs actual shares in donut charts
with col2:
    plot_pie_chart(portfolio=st.session_state.portfolio, ticker_list=ticker_list)
