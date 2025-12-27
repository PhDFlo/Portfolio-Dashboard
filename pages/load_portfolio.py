import streamlit as st
import pandas as pd
from foliotrack.Portfolio import Portfolio
from dashboard import (
    load_data_config,
    loadportfolio2df,
    save_portfolio_to_file,
    side_bar_file_operations,
    table_section,
    buy_section,
    sell_section,
    save_section,
    get_security_historical_data,
    plot_pie_chart,
    plot_portfolio_evolution,
)

# Side bar for file operations
file_list = side_bar_file_operations()

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
    with col_pie:
        plot_pie_chart(portfolio=st.session_state.portfolio, ticker_list=ticker_list)

# Portfolio table
if st.session_state.portfolio.securities:
    st.session_state.df = loadportfolio2df(st.session_state.portfolio)
else:
    # Create empty dataframe with proper structure
    st.session_state.df = pd.DataFrame(
        {
            "Name": [""],
            "Ticker": [""],
            "Currency": ["EUR"],
            "Price": [0.0],
            "Actual Share": [0.0],
            "Target Share": [0.0],
            f"Amount Invested ({st.session_state.portfolio.symbol})": [0.0],
            "Number Held": [0.0],
        }
    )

# List of tickers for buy and sell
ticker_options = [""] + ticker_list

st.subheader("Security List")
table_section()

# Buy and sell section
col_buy, col_sell = st.columns(2)
with col_buy:
    st.subheader("Buy Security")
    buy_section(ticker_options)


with col_sell:
    st.subheader("Sell Security")
    sell_section(ticker_options)


# Save portfolio section
st.subheader("Save Portfolio")
col_save, _ = st.columns(2)
with col_save:
    save_section(file_list)
