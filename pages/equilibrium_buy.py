import streamlit as st
from dashboard import plot_equilibrium

# Optimization parameters
st.subheader("Optimization")

selling = st.checkbox(
    "Allow Selling Securities",
    key="allow_selling",
    value=False,
)

col1, col2 = st.columns(2)
with col1:
    new_investment = st.number_input(
        "New Investment Amount (€)",
        key="investment_amount",
        value=500.0,
        min_value=0.0,
        format="%.2f",
    )
with col2:
    min_percent = st.number_input(
        "Minimum Percentage to Invest",
        key="min_percent",
        value=0.99,
        min_value=0.0,
        max_value=1.0,
        format="%.2f",
    )

# List of tickers for buy and sell
if "ticker_options" not in st.session_state:
    st.session_state.ticker_options = [""]
    st.session_state.file_list = [""]


# Optimization button and results
plot_equilibrium(
    new_investment,
    min_percent,
    selling,
    st.session_state.ticker_options,
    st.session_state.file_list,
)
