import streamlit as st
from dashboard import (
    side_bar_file_operations,
    plot_backtest,
)
from datetime import date
from foliotrack.services.MarketService import MarketService

# Side bar for file operations
side_bar_file_operations()

begin_date = st.sidebar.date_input(
    "Backtest start date (YYYY-MM-DD)",
    value=date(2010, 1, 1).strftime("%Y-%m-%d"),
    key="bt_begin_date",
    format="YYYY-MM-DD",
)

end_date = st.sidebar.date_input(
    "Backtest end date (YYYY-MM-DD)",
    value=date.today().strftime("%Y-%m-%d"),
    key="bt_end_date",
    format="YYYY-MM-DD",
)

market_service = MarketService("ffn")

if "portfolio" in st.session_state:
    plot_backtest(st.session_state.portfolio, market_service, begin_date, end_date)

st.subheader("Backtest")
