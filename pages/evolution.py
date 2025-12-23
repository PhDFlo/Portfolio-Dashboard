import streamlit as st
from dashboard import (
    side_bar_file_operations,
)
from foliotrack.Portfolio import Portfolio
from dashboard.utils_evolution import (
    get_historical_data,
    plot_pie_chart,
    plot_portfolio_evolution,
)
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


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
