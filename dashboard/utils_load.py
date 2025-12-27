import streamlit as st
from foliotrack.Portfolio import Portfolio
import pandas as pd
import os
import glob

load_data_config = {
    "Name": st.column_config.TextColumn("Name", width="large"),
    "Ticker": st.column_config.TextColumn("Ticker", width="small"),
    "Currency": st.column_config.TextColumn("Currency", width="small"),
    "Price": st.column_config.NumberColumn("Price", format="%.4f"),
    "Actual Share": st.column_config.NumberColumn("Actual Share", format="%.4f"),
    "Target Share": st.column_config.NumberColumn("Target Share", format="%.4f"),
    f"Total value ({st.session_state.portfolio.symbol})": st.column_config.NumberColumn(
        f"Total value ({st.session_state.portfolio.symbol})", format="%.2f"
    ),
    "Volume": st.column_config.NumberColumn("Volume", format="%.0f"),
}


def get_portfolio_files() -> list:
    """Get list of JSON files in Portfolios directory"""
    if not os.path.exists("./Portfolios"):
        os.makedirs("./Portfolios", exist_ok=True)
    return glob.glob("./Portfolios/*.json")


def loadportfolio2df(portfolio) -> pd.DataFrame:
    """Convert portfolio info to DataFrame format for display"""
    info = portfolio.get_portfolio_info()
    data = []
    for security in info:
        data.append(
            {
                "Name": security.get("name"),
                "Ticker": security.get("ticker"),
                "Currency": security.get("currency"),
                "Price": security.get("price_in_security_currency"),
                "Actual Share": security.get("actual_share"),
                "Target Share": security.get("target_share"),
                f"Total value ({portfolio.symbol})": security.get("value"),
                "Volume": security.get("volume"),
            }
        )
    return pd.DataFrame(data)


@st.cache_data
def load_portfolio_from_file(filename) -> Portfolio:
    """Load portfolio from JSON file"""
    try:
        portfolio = Portfolio.from_json(filename)
        return portfolio
    except Exception as e:
        st.error(f"Error loading portfolio: {str(e)}")
        return Portfolio()


def save_portfolio_to_file(filename) -> bool:
    """Save portfolio to JSON file"""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        st.session_state.portfolio.to_json(filename)
        st.success(f"Portfolio saved to {filename}")
        return True
    except Exception as e:
        st.error(f"Error saving portfolio: {str(e)}")
        return False


# Put fragment to avoid reloading the full page each time selectbox value is changed
@st.fragment
def _selectbox_file(file_list, key) -> str:
    return st.selectbox(
        "Select Portfolio JSON",
        options=file_list,
        key=key,
        index=1 if len(file_list) > 1 and "investment_example.json" in file_list else 0,
        accept_new_options=True,
    )


def side_bar_file_operations(key="portfolio_file_select") -> list:
    """Sidebar for file operations"""
    with st.sidebar:
        st.header("Portfolio Files")

        # File selection
        portfolio_files = get_portfolio_files()
        file_list = [""] + [os.path.basename(f) for f in portfolio_files]

        selected_file = _selectbox_file(file_list, key)

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

    return file_list


@st.fragment
def table_section():
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
            # st.rerun()
        except Exception as e:
            st.error(f"Error updating prices: {str(e)}")


@st.fragment
def buy_section(ticker_options):
    col1, col2 = st.columns(2)
    with col1:
        ticker_input_buy = st.selectbox(
            "Security ticker",
            options=ticker_options,
            key="ticker_buy_choice",
            index=1 if len(ticker_options) > 1 else 0,
            accept_new_options=True,
        )

        # Set default currency and value based on selected ticker
        default_currency = st.session_state.portfolio.currency
        default_buy_price = 0.0
        if len(st.session_state.portfolio.securities) != 0:
            default_currency = st.session_state.portfolio.securities[
                ticker_input_buy
            ].currency
            default_buy_price = st.session_state.portfolio.securities[
                ticker_input_buy
            ].price_in_security_currency

        volume_buy = st.number_input(
            "Volume to Buy",
            key="buy_volume",
            value=1.0,
            min_value=0.0,
            format="%.1f",
            step=1.0,
        )

    with col2:
        currency = st.text_input(
            "Security Currency", key="buy_currency", value=default_currency
        )

        buy_price = st.number_input(
            "Unit Price",
            key="buy_price",
            value=default_buy_price,
            min_value=0.0,
            format="%.2f",
        )

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
            # st.rerun()
        except Exception as e:
            st.error(f"Error buying security: {str(e)}")


@st.fragment
def sell_section(ticker_options):
    ticker_input_sell = st.selectbox(
        "Security ticker to sell",
        options=ticker_options,
        key="ticker_sell_choice",
        index=1 if len(ticker_options) > 1 else 0,
        accept_new_options=True,
    )
    volume_sell = st.number_input(
        "Volume to Sell",
        key="sell_volume",
        value=1.0,
        min_value=0.0,
        format="%.1f",
        step=1.0,
    )

    if st.button("📤 Sell Security", key="sell_button", use_container_width=True):
        try:
            st.session_state.portfolio.sell_security(
                ticker=ticker_input_sell,
                volume=volume_sell,
            )
            st.success(f"Sold {volume_sell} unit(s) of {ticker_input_sell}")
            # st.rerun()
        except Exception as e:
            st.error(f"Error selling security: {str(e)}")


@st.fragment
def save_section(file_list):
    save_filename = st.selectbox(
        "Save as filename",
        options=file_list,
        key="portfolio_file_save",
        index=1 if len(file_list) > 1 and "investment_example.json" in file_list else 0,
        accept_new_options=True,
    )

    if st.button("💾 Save Portfolio", key="save_button", use_container_width=True):
        save_portfolio_to_file(f"./Portfolios/{save_filename}")
