import streamlit as st
import pandas as pd
from src.ui.components.sidebar import render_sidebar
from src.ui.components.plots import plot_pie_chart, plot_portfolio_evolution
from src.services.market_service import MarketService

# Initialize services
market_service = MarketService()

# Title and Metrics
st.title(f"📊 {st.session_state.portfolio.name}")

# Calculate high-level stats
total_value = st.session_state.portfolio.total_value
num_securities = len(st.session_state.portfolio.securities)
symbol = st.session_state.portfolio.symbol

# Premium KPI Row
with st.container(border=True):
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric("Total Portfolio Value", f"{total_value:,.2f} {symbol}")
    with m_col2:
        st.metric("Total Securities", num_securities)
    with m_col3:
        st.metric("Base Currency", st.session_state.portfolio.currency)

# Side bar for file operations
render_sidebar()

with st.sidebar:
    st.divider()
    st.subheader("Chart Settings")
    min_y_exchange = st.number_input(
        "Min Y (Buy/Sell Plot)",
        value=-5,
    )
    max_y_exchange = st.number_input(
        "Max Y (Buy/Sell Plot)",
        value=20,
    )

# List of tickers
ticker_list = list(st.session_state.portfolio.securities.keys())

# Main Display Area
if ticker_list:
    col_candle, col_pie = st.columns([2, 1])

    with col_candle:
        with st.container(border=True):
            # Check if history exists
            if (
                hasattr(st.session_state.portfolio, "history")
                and st.session_state.portfolio.history
            ):
                start_date = min(
                    event["date"] for event in st.session_state.portfolio.history
                )

                # Get historical data for all tickers in portfolio
                with st.spinner("Fetching historical data..."):
                    hist_tickers = market_service.get_security_historical_data(
                        ticker_list, start_date=start_date
                    )

                if not hist_tickers.empty:
                    plot_portfolio_evolution(
                        portfolio=st.session_state.portfolio,
                        ticker_list=ticker_list,
                        hist_tickers=hist_tickers,
                        Date=pd.DatetimeIndex(hist_tickers.index),
                        min_y_exchange=min_y_exchange,
                        max_y_exchange=max_y_exchange,
                    )
                else:
                    st.info("No historical data available for these tickers.")
            else:
                st.info("No history available for this portfolio. Add some transactions to see evolution.")

    with col_pie:
        with st.container(border=True):
            plot_pie_chart(portfolio=st.session_state.portfolio, ticker_list=ticker_list)
else:
    st.info("Your portfolio is currently empty. Go to 'Portfolio & Update Prices' to load or add securities.")
