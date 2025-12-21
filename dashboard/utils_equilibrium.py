import streamlit as st
import pandas as pd

eq_data_config = {
    "Name": st.column_config.TextColumn("Name"),
    "Ticker": st.column_config.TextColumn("Ticker"),
    "Currency": st.column_config.TextColumn("Currency"),
    "Price": st.column_config.NumberColumn("Price", format="%.4f"),
    "Target Share": st.column_config.NumberColumn("Target Share", format="%.4f"),
    "Actual Share": st.column_config.NumberColumn("Actual Share", format="%.4f"),
    "Final Share": st.column_config.NumberColumn("Final Share", format="%.4f"),
    "Amount to Invest": st.column_config.NumberColumn(
        "Amount to Invest", format="%.2f"
    ),
    "Volume to buy": st.column_config.NumberColumn("Volume to buy", format="%.0f"),
}


def eqportfolio2df(portfolio) -> pd.DataFrame:
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
                "Target Share": security.get("target_share"),
                "Actual Share": security.get("actual_share"),
                "Final Share": security.get("final_share"),
                "Amount to Invest": security.get("amount_to_invest"),
                "Volume to buy": security.get("volume_to_buy"),
            }
        )
    return pd.DataFrame(data)
