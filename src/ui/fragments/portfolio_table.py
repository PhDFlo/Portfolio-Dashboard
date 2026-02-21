import streamlit as st
from src.services.data_service import DataService
from src.services.market_service import MarketService

# Initialize services
market_service = MarketService()

LOAD_DATA_CONFIG = {
    "Name": st.column_config.TextColumn("Name", width="large"),
    "Ticker": st.column_config.TextColumn("Ticker", width="small"),
    "Currency": st.column_config.TextColumn("Currency", width="small"),
    "Price": st.column_config.NumberColumn("Price", format="%.4f"),
    "Actual Share": st.column_config.NumberColumn("Actual Share", format="%.4f"),
    "Target Share": st.column_config.NumberColumn("Target Share", format="%.4f"),
    "Total": st.column_config.NumberColumn("Total value", format=None),
    "Volume": st.column_config.NumberColumn("Volume", format="%.0f"),
}


@st.fragment
def render_portfolio_table():
    """Renders the portfolio table and update price button as a fragment"""

    # Portfolio table conversion
    # We rely on st.session_state.portfolio being present
    if "portfolio" not in st.session_state:
        st.error("No portfolio loaded.")
        return

    df = DataService.portfolio_to_df(st.session_state.portfolio)

    st.data_editor(
        df,
        num_rows="dynamic",
        width="stretch",
        column_config=LOAD_DATA_CONFIG,
        key="portfolio_editor",
    )

    if st.button(
        "💰 Update Securities Price",
        key="update_securities_price",
        width="stretch",
    ):
        try:
            with st.spinner("Updating prices..."):
                market_service.update_prices(st.session_state.portfolio)
            st.success("Security prices updated!")
            st.rerun(scope="fragment")
        except Exception as e:
            st.error(f"Error updating prices: {str(e)}")
