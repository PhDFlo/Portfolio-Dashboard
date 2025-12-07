import streamlit as st
import pandas as pd
import os
from foliotrack.Portfolio import Portfolio
from dashboard import (
    loadportfolio2df,
    load_portfolio_from_file,
    save_portfolio_to_file,
    get_portfolio_files,
    load_data_config,
)


# Sidebar for file operations
with st.sidebar:
    st.header("Portfolio Files")

    # File selection
    portfolio_files = get_portfolio_files()
    file_options = [""] + [os.path.basename(f) for f in portfolio_files]

    selected_file = st.selectbox(
        "Select Portfolio JSON",
        options=file_options,
        key="portfolio_file_select",
        index=1
        if len(file_options) > 1 and "investment_example.json" in file_options
        else 0,
        accept_new_options=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh", key="refresh"):
            st.rerun()

    with col2:
        if st.button("📂 Load", key="load") and selected_file:
            st.session_state.portfolio = load_portfolio_from_file(
                f"./Portfolios/{selected_file}"
            )
            st.rerun()

# Display current portfolio in editable table
if "portfolio" not in st.session_state:
    # Ensure a portfolio object exists in session state for pages run standalone
    st.session_state.portfolio = Portfolio()

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
ticker_options = [""] + [ticker for ticker in st.session_state.portfolio.securities]

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
        options=file_options,
        key="portfolio_file_save",
        index=1
        if len(file_options) > 1 and "investment_example.json" in file_options
        else 0,
        accept_new_options=True,
    )

    if st.button("💾 Save Portfolio", key="save_button", use_container_width=True):
        save_portfolio_to_file(f"./Portfolios/{save_filename}")
