import streamlit as st
from src.services.backtest_service import BacktestServiceWrapper


@st.fragment
def render_backtest_view(portfolio, market_service, begin_date, end_date):
    if st.button("🎬 Run backtest", key="optimize_button", width="stretch"):
        try:
            backtest_service = BacktestServiceWrapper()
            result = backtest_service.run_backtest(
                portfolio, market_service, begin_date, end_date
            )
            st.text(result.display())
            st.rerun(scope="fragment")
        except Exception as e:
            st.error(f"Backtest computation failed: {e}")
