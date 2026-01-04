import streamlit as st
import pandas as pd
from foliotrack.domain.Portfolio import Portfolio
from src.ui.components.sidebar import render_sidebar
from src.ui.components.plots import plot_pie_chart, plot_portfolio_evolution
from src.services.market_service import MarketService

# Initialize services
market_service = MarketService()

# Side bar for file operations
render_sidebar()

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

# List of tickers
ticker_list = [ticker for ticker in st.session_state.portfolio.securities]

# Display Portfolio statistics plots
col_candle, col_pie = st.columns([3, 1])

# If there is at least one ticker
if ticker_list != []:
    # Display portfolio value evolution over time
    with col_candle:
        # Check if history exists
        if (
            hasattr(st.session_state.portfolio, "history")
            and st.session_state.portfolio.history
        ):
            start_date = min(
                event["date"] for event in st.session_state.portfolio.history
            )

            # Get historical data for all tickers in portfolio
            hist_tickers = market_service.get_security_historical_data(
                ticker_list, start_date=start_date, interval="1d"
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
            st.info("No history available for this portfolio.")

    # Display target vs actual shares in donut charts
    with col_pie:
        plot_pie_chart(portfolio=st.session_state.portfolio, ticker_list=ticker_list)
