import streamlit as st
import pandas as pd
import datetime
from .utils import (
    load_portfolio_data,
    update_portfolio_from_dataframe,
    save_portfolio_to_file,
)

# Configure page
st.set_page_config(
    page_title="Security Portfolio Optimizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.header("Portfolio Management")

# Display current portfolio in editable table
if st.session_state.portfolio.securities:
    df = load_portfolio_data(st.session_state.portfolio)
else:
    # Create empty dataframe with proper structure
    df = pd.DataFrame(
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

edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Name": st.column_config.TextColumn("Name", width="medium"),
        "Ticker": st.column_config.TextColumn("Ticker", width="small"),
        "Currency": st.column_config.TextColumn("Currency", width="small"),
        "Price": st.column_config.NumberColumn("Price", format="%.4f"),
        "Actual Share": st.column_config.NumberColumn("Actual Share", format="%.4f"),
        "Target Share": st.column_config.NumberColumn("Target Share", format="%.4f"),
        f"Amount Invested ({st.session_state.portfolio.symbol})": st.column_config.NumberColumn(
            f"Amount Invested ({st.session_state.portfolio.symbol})", format="%.2f"
        ),
        "Number Held": st.column_config.NumberColumn("Number Held", format="%.0f"),
    },
    key="portfolio_editor",
)
# Update portfolio if data was edited
if not edited_df.equals(df):
    update_portfolio_from_dataframe(edited_df)

# Action buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("💰 Update Security Prices", use_container_width=True):
        try:
            st.session_state.portfolio.update_security_prices()
            st.session_state.portfolio.compute_actual_shares()
            st.success("Security prices updated!")
            st.rerun()
        except Exception as e:
            st.error(f"Error updating prices: {str(e)}")
with col2:
    if st.button("🔄 Refresh Portfolio Display", use_container_width=True):
        st.rerun()
# Save portfolio section
st.subheader("Save Portfolio")
col1, col2 = st.columns([3, 1])
with col1:
    default_filename = (
        f"Portfolios/investment_{datetime.datetime.now().strftime('%d_%m_%Y')}.json"
    )
    save_filename = st.text_input("Save as filename", value=default_filename)
with col2:
    st.write("")  # Add spacing
    st.write("")  # Add spacing
    if st.button("💾 Save Portfolio"):
        save_portfolio_to_file(save_filename)
