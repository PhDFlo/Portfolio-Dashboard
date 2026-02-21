import streamlit as st
from src.services.optimization_service import OptimizationService
from src.services.data_service import DataService
from src.ui.fragments.portfolio_actions import render_portfolio_actions

# Initialize services
optimizer = OptimizationService()

EQ_DATA_CONFIG = {
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


@st.fragment
def render_equilibrium_view(
    new_investment, min_percent, max_diff_sec, selling, ticker_options, file_list
):
    """Renders the equilibrium optimization view"""

    # Create empty dataframe with proper structure
    if st.session_state.portfolio.securities:
        equilibrium_df = DataService.equilibrium_to_df(st.session_state.portfolio)
    else:
        # Fallback empty df
        equilibrium_df = DataService.equilibrium_to_df(
            st.session_state.portfolio
        )  # DataService handles empty

    if st.button("🎯 Optimize Portfolio", key="optimize_button", width="stretch"):
        try:
            # Run optimization
            _, st.session_state.total_to_invest, _ = optimizer.solve_equilibrium(
                st.session_state.portfolio,
                investment_amount=float(new_investment),
                min_percent_to_invest=float(min_percent),
                max_different_securities=int(max_diff_sec),
                selling=bool(selling),
            )

            st.session_state.optim_ran = True
            st.rerun(scope="fragment")

        except Exception as e:
            if 'scope="fragment"' in str(e):
                st.rerun()
            else:
                st.error(f"Error during optimization: {str(e)}")

    if "optim_ran" in st.session_state:
        st.dataframe(
            equilibrium_df,
            width="stretch",
            column_config=EQ_DATA_CONFIG,
        )

        # Display Total to invest if available
        if hasattr(st.session_state, "total_to_invest"):
            st.write(
                f"Total to Invest: {st.session_state.total_to_invest:.2f} {st.session_state.portfolio.symbol}"
            )

    # Re-use portfolio actions
    render_portfolio_actions(ticker_options, file_list)
