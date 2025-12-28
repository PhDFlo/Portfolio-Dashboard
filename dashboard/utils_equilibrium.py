import streamlit as st
import pandas as pd
from foliotrack.Equilibrate import solve_equilibrium
from .utils_load import _buy_box, _sell_box, _save_box

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


@st.fragment
def plot_equilibrium(new_investment, min_percent, selling, ticker_options, file_list):
    # Create empty dataframe with proper structure
    if st.session_state.portfolio.securities:
        equilibrium_df = eqportfolio2df(st.session_state.portfolio)
    else:
        equilibrium_df = pd.DataFrame(
            {
                "Name": [""],
                "Ticker": [""],
                "Currency": ["EUR"],
                "Price": [0.0],
                "Target Share": [0.0],
                "Actual Share": [0.0],
                "Final Share": [0.0],
                "Amount to invest": [0.0],
                "Volume to buy": [0.0],
            }
        )

    if st.button("🎯 Optimize Portfolio", key="optimize_button", width="stretch"):
        try:
            # Run optimization
            _, st.session_state.total_to_invest, _ = solve_equilibrium(
                st.session_state.portfolio,
                investment_amount=float(new_investment),
                min_percent_to_invest=float(min_percent),
                selling=bool(selling),
            )

            st.session_state.optim_ran = True
            st.rerun(scope="fragment")

        except Exception as e:
            st.error(f"Error during optimization: {str(e)}")

    if "optim_ran" in st.session_state:
        st.dataframe(
            equilibrium_df,
            width="stretch",
            column_config=eq_data_config,
        )

        st.write(
            f"Total to Invest: {st.session_state.total_to_invest:.2f} {st.session_state.portfolio.symbol}"
        )

    # Buy and sell section
    col_buy, col_sell = st.columns(2)

    # Buy security
    with col_buy:
        st.subheader("Buy Security")
        _buy_box(ticker_options)

    # Sell security
    with col_sell:
        st.subheader("Sell Security")
        _sell_box(ticker_options)

    # Save portfolio section
    st.subheader("Save Portfolio")
    col_save, _ = st.columns(2)
    with col_save:
        _save_box(file_list)
