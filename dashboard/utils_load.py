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


def load_portfolio_from_file(filename) -> Portfolio:
    """Load portfolio from JSON file"""
    try:
        portfolio = Portfolio.from_json(filename)
        st.success(f"Portfolio loaded from {filename}")
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


def side_bar_file_operations(key="portfolio_file_select") -> list:
    """Sidebar for file operations"""
    with st.sidebar:
        st.header("Portfolio Files")

        # File selection
        portfolio_files = get_portfolio_files()
        file_list = [""] + [os.path.basename(f) for f in portfolio_files]

        selected_file = st.selectbox(
            "Select Portfolio JSON",
            options=file_list,
            key=key,
            index=1
            if len(file_list) > 1 and "investment_example.json" in file_list
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

    return file_list
