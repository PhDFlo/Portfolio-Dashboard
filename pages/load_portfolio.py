import streamlit as st
import pandas as pd
import os
import datetime
from dashboard.utils import (
    load_portfolio_data,
    load_portfolio_from_file,
    update_portfolio_from_dataframe,
    save_portfolio_to_file,
    get_portfolio_files,
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
        index=1
        if len(file_options) > 1 and "investment_example.json" in file_options
        else 0,
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh"):
            st.rerun()

    with col2:
        if st.button("📂 Load") and selected_file:
            load_portfolio_from_file(f"./Portfolios/{selected_file}")
            st.rerun()

# Display current portfolio in editable table
if st.session_state.portfolio.securities:
    st.session_state.df = load_portfolio_data(st.session_state.portfolio)
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

st.session_state.edited_df = st.data_editor(
    st.session_state.df,
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
if not st.session_state.edited_df.equals(st.session_state.df):
    update_portfolio_from_dataframe(st.session_state.edited_df)

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
