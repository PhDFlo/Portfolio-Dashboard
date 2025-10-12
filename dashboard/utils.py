import streamlit as st
from foliotrack.Security import Security
from foliotrack.Portfolio import Portfolio
import pandas as pd
import os
import glob


def get_portfolio_files():
    """Get list of JSON files in Portfolios directory"""
    if not os.path.exists("./Portfolios"):
        os.makedirs("./Portfolios", exist_ok=True)
    return glob.glob("./Portfolios/*.json")


def load_portfolio_data(portfolio):
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
                f"Amount Invested ({portfolio.symbol})": security.get(
                    "amount_invested"
                ),
                "Number Held": security.get("number_held"),
            }
        )
    return pd.DataFrame(data)


def load_portfolio_from_file(filename):
    """Load portfolio from JSON file"""
    try:
        st.session_state.portfolio = Portfolio.from_json(filename)
        st.success(f"Portfolio loaded from {filename}")
        return True
    except Exception as e:
        st.error(f"Error loading portfolio: {str(e)}")
        return False


def save_portfolio_to_file(filename):
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


def update_portfolio_from_dataframe(df):
    """Update portfolio object from edited dataframe"""
    st.session_state.portfolio.securities.clear()
    for _, row in df.iterrows():
        if pd.notna(row["Name"]) and pd.notna(row["Ticker"]):
            security = Security(
                name=str(row["Name"]),
                ticker=str(row["Ticker"]),
                currency=str(row["Currency"]) if pd.notna(row["Currency"]) else "EUR",
                price_in_security_currency=float(row["Price"])
                if pd.notna(row["Price"])
                else 0.0,
                actual_share=float(row["Actual Share"])
                if pd.notna(row["Actual Share"])
                else 0.0,
                target_share=float(row["Target Share"])
                if pd.notna(row["Target Share"])
                else 0.0,
                number_held=float(row["Number Held"])
                if pd.notna(row["Number Held"])
                else 0.0,
            )
            st.session_state.portfolio.add_security(security)
