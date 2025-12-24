import streamlit as st
import pandas as pd
from foliotrack.Portfolio import Portfolio
from dashboard import (
    loadportfolio2df,
    save_portfolio_to_file,
    load_data_config,
    side_bar_file_operations,
)
from dashboard.utils_evolution import (
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


tab1, tab2 = st.tabs(["Display statistics", "Table"])

with tab1:
    ticker_list = [ticker for ticker in st.session_state.portfolio.securities]

    col1, col2 = st.columns([3, 1])

    # If there is at least one ticker
    if ticker_list != []:
        # Display portfolio value evolution over time
        with col1:
            start_date = min(
                event["date"] for event in st.session_state.portfolio.history
            )

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
        with col2:
            plot_pie_chart(
                portfolio=st.session_state.portfolio, ticker_list=ticker_list
            )


with tab2:
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

    st.data_editor(
        st.session_state.df,
        num_rows="dynamic",
        use_container_width=True,
        column_config=load_data_config,
        key="portfolio_editor",
    )
    # Update security prices
    if st.button(
        "💰 Update Securities Price",
        key="update_securities_price",
        use_container_width=True,
    ):
        try:
            st.session_state.portfolio.update_portfolio()
            st.success("Security prices updated!")
            st.rerun()
        except Exception as e:
            st.error(f"Error updating prices: {str(e)}")

    # Buy and sell section
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Buy Security")
        ticker_input_buy = st.selectbox(
            "Security ticker",
            options=ticker_options,
            key="ticker_buy_choice",
            index=1 if len(ticker_options) > 1 else 0,
            accept_new_options=True,
        )
        volume_buy = st.number_input(
            "Volume to Buy", key="buy_volume", value=1.0, format="%.1f", step=1.0
        )

        # Set default currency and value based on selected ticker
        default_currency = st.session_state.portfolio.currency
        default_buy_price = 0.0
        for ticker, security in st.session_state.portfolio.securities.items():
            if ticker_input_buy == ticker:
                default_currency = security.currency
                default_buy_price = security.price_in_security_currency
                break

        currency = st.text_input(
            "Security Currency", key="buy_currency", value=default_currency
        )
        buy_price = st.number_input(
            "Unit Price", key="buy_price", value=default_buy_price, format="%.2f"
        )

    with col2:
        st.subheader("Sell Security")
        ticker_input_sell = st.selectbox(
            "Security ticker to sell",
            options=ticker_options,
            key="ticker_sell_choice",
            index=1 if len(ticker_options) > 1 else 0,
            accept_new_options=True,
        )
        volume_sell = st.number_input(
            "Volume to Sell", key="sell_volume", value=1.0, format="%.1f", step=1.0
        )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Buy Security", key="buy_button", use_container_width=True):
            try:
                st.session_state.portfolio.buy_security(
                    ticker=ticker_input_buy,
                    volume=volume_buy,
                    price=buy_price,
                    currency=currency,
                )
                st.success(
                    f"Bought {volume_buy} unit(s) of {ticker_input_buy} at {buy_price}"
                )
                st.rerun()
            except Exception as e:
                st.error(f"Error buying security: {str(e)}")

    with col2:
        if st.button("📤 Sell Security", key="sell_button", use_container_width=True):
            try:
                st.session_state.portfolio.sell_security(
                    ticker=ticker_input_sell,
                    volume=volume_sell,
                )
                st.success(f"Sold {volume_sell} unit(s) of {ticker_input_sell}")
                st.rerun()
            except Exception as e:
                st.error(f"Error selling security: {str(e)}")

    # Save portfolio section
    st.subheader("Save Portfolio")
    col1, col2 = st.columns(2)
    with col1:
        save_filename = st.selectbox(
            "Save as filename",
            options=file_list,
            key="portfolio_file_save",
            index=1
            if len(file_list) > 1 and "investment_example.json" in file_list
            else 0,
            accept_new_options=True,
        )

        if st.button("💾 Save Portfolio", key="save_button", use_container_width=True):
            save_portfolio_to_file(f"./Portfolios/{save_filename}")
