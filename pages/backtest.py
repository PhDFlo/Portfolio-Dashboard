import streamlit as st
from datetime import date
from foliotrack.services import MarketService
from src.ui.components.sidebar import render_sidebar
from src.ui.fragments.backtest_view import render_backtest_view

st.title("📊 Backtest Simulation")

# Side bar for file operations
render_sidebar()

with st.sidebar:
    st.divider()
    st.header("Backtest Period")
    begin_date = st.date_input(
        "Start Date",
        value=date(2010, 1, 1),
        key="bt_begin_date",
        format="YYYY-MM-DD",
    )

    end_date = st.date_input(
        "End Date",
        value=date.today(),
        key="bt_end_date",
        format="YYYY-MM-DD",
    )

market_service = MarketService()

if "portfolio" in st.session_state:
    render_backtest_view(
        st.session_state.portfolio, market_service, begin_date, end_date
    )

st.subheader("Backtest")
