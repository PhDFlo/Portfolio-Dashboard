import streamlit as st
import pandas as pd
from foliotrack.domain.Portfolio import Portfolio
from foliotrack.services.BacktestService import BacktestService


@st.cache_data
def _run_backtest(portfolio: Portfolio, _market_service, begin_date, end_date):
    backtester = BacktestService()
    result = backtester.run_backtest(
        portfolio,
        _market_service,
        start_date=begin_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
    )
    return result


@st.fragment
def plot_backtest(portfolio: Portfolio, market_service, begin_date, end_date):
    if st.button("🎬 Run backtest", key="optimize_button", width="stretch"):
        try:
            result = _run_backtest(portfolio, market_service, begin_date, end_date)
            st.text(result.display())
            st.rerun(scope="fragment")
        except Exception as e:
            st.error(f"Backtest computation failed: {e}")
