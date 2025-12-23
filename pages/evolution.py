import streamlit as st
import pandas as pd
from dashboard import (
    side_bar_file_operations,
)
from foliotrack.Portfolio import Portfolio
from dashboard.utils_evolution import (
    plot_pie_chart,
    plot_portfolio_evolution,
)


# Side bar for file operations
side_bar_file_operations()

# Sidebar input
start_date = st.sidebar.date_input(
    "Start Date",
    format="YYYY-MM-DD",
    value=pd.to_datetime("2023-01-01"),
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
        plot_portfolio_evolution(
            portfolio=st.session_state.portfolio,
            ticker_list=ticker_list,
            start_date=str(start_date),
        )

# Display target vs actual shares in donut charts
with col2:
    plot_pie_chart(portfolio=st.session_state.portfolio, ticker_list=ticker_list)
