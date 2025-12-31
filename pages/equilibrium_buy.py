import streamlit as st
from dashboard import plot_equilibrium

# Optimization parameters
st.subheader("Optimization")

selling = st.checkbox(
    "Allow Selling Securities",
    key="allow_selling",
    value=False,
)

col_amount, col_percent, col_max_sec = st.columns(3)
with col_amount:
    new_investment = st.number_input(
        "New Investment Amount (€)",
        key="investment_amount",
        value=500.0,
        min_value=0.0,
        format="%.2f",
    )
with col_percent:
    min_percent = st.number_input(
        "Minimum Percentage to Invest",
        key="min_percent",
        value=0.99,
        min_value=0.0,
        max_value=1.0,
        format="%.2f",
    )
with col_max_sec:
    max_diff_sec = st.number_input(
        "Maximum number of different securities",
        key="max_diff_sec",
        value=3,
        min_value=0,
        max_value=1000,
        format="%i",
    )

# List of tickers for buy and sell
if "ticker_options" not in st.session_state:
    st.session_state.ticker_options = [""]
    st.session_state.file_list = [""]


# Optimization button and results
plot_equilibrium(
    new_investment,
    min_percent,
    max_diff_sec,
    selling,
    st.session_state.ticker_options,
    st.session_state.file_list,
)
