import streamlit as st
import pandas as pd

eq_data_config = {
    "Price": st.column_config.NumberColumn("Price", format="%.4f"),
    "Target Share": st.column_config.NumberColumn("Target Share", format="%.4f"),
    "Actual Share": st.column_config.NumberColumn("Actual Share", format="%.4f"),
    "Final Share": st.column_config.NumberColumn("Final Share", format="%.4f"),
    "Amount to Invest": st.column_config.NumberColumn(
        "Amount to Invest", format="%.2f"
    ),
    "Number to buy": st.column_config.NumberColumn("Number to buy", format="%.0f"),
}


# Need to update method to include actual share and final share
#                "Target Share": security.get("target_share"),
#                "Actual Share": security.get("actual_share"),
#                "Final Share": security.get("final_share"),
def eqportfolio2df(portfolio):
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
                "Amount to Invest": security.get("amount_to_invest"),
                "Number to buy": security.get("number_to_buy"),
            }
        )
    return pd.DataFrame(data)
