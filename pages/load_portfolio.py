import streamlit as st
import pandas as pd
import os
import datetime
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
        
# Buy and sell section
col1, col2 = st.columns(2)

with col1:
    st.subheader("Buy Security")
    ticker_input = st.text_input("Security Ticker")
    quantity = st.number_input("Quantity to Buy", value=1.0, format="%.1f", step=1.0)
    currency = st.text_input("Security Currency", value="EUR")
    buy_price = st.number_input("Unit Price", format="%.2f")
            
with col2:
    st.subheader("Sell Security")
    ticker_input_sell = st.text_input("Security Ticker to Sell", key="sell_ticker")
    quantity_sell = st.number_input(
        "Quantity to Sell", value=1.0, format="%.1f", step=1.0, key="sell_quantity"
    )
            
with col1:
    if st.button("💸 Buy Security"):
        try:
            st.session_state.portfolio.buy_security(
                ticker=ticker_input,
                quantity=quantity,
                price=buy_price,
                currency=currency,
            )
            st.success(f"Bought {quantity} unit(s) of {ticker_input} at {buy_price}")
            st.rerun()
        except Exception as e:
            st.error(f"Error buying security: {str(e)}")
            
with col2:
    if st.button("💵 Sell Security"):
        try:
            st.session_state.portfolio.sell_security(
                ticker=ticker_input_sell,
                quantity=quantity_sell,
            )
            st.success(f"Sold {quantity_sell} unit(s) of {ticker_input_sell}")
            st.rerun()
        except Exception as e:
            st.error(f"Error selling security: {str(e)}")
        
# Save portfolio section
st.subheader("Save Portfolio")
col1, col2 = st.columns([3, 1])
with col1:
    default_filename = (
        f"Portfolios/investment_{datetime.datetime.now().strftime('%d_%m_%Y')}.json"
    )
    save_filename = st.text_input(
        "Save as filename", value=default_filename, key="save_filename"
    )
with col2:
    st.write("")  # Add spacing
    st.write("")  # Add spacing
    if st.button("💾 Save Portfolio", key="save_button"):
        save_portfolio_to_file(save_filename)
