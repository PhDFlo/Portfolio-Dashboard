import streamlit as st
from datetime import date
from foliotrack.services.MarketService import MarketService
from foliotrack.storage.PortfolioRepository import PortfolioRepository
from src.config import PORTFOLIOS_DIR

# Initialize services
market_service = MarketService()
repo = PortfolioRepository()


@st.fragment
def render_portfolio_actions(ticker_options: list, file_list: list):
    """Renders the Buy, Sell and Save actions as a fragment"""

    col_buy, col_sell = st.columns(2)

    # Buy security
    with col_buy:
        st.subheader("Buy Security")
        _render_buy_box(ticker_options)

    # Sell security
    with col_sell:
        st.subheader("Sell Security")
        _render_sell_box(ticker_options)

    # Save portfolio section
    st.subheader("Save Portfolio")
    col_save, _ = st.columns(2)
    with col_save:
        _render_save_box(file_list)


def _render_buy_box(ticker_options):
    col1, col2 = st.columns(2)
    with col1:
        ticker_input_buy = st.selectbox(
            "Security ticker",
            options=ticker_options,
            key="ticker_buy_choice",
            index=1 if len(ticker_options) > 1 else 0,
            accept_new_options=True,
        )

        # Set default currency and value based on selected ticker
        default_currency = st.session_state.portfolio.currency
        if (
            len(st.session_state.portfolio.securities) != 0
            and ticker_input_buy in st.session_state.portfolio.securities
        ):
            default_currency = st.session_state.portfolio.securities[
                ticker_input_buy
            ].currency

        volume_buy = st.number_input(
            "Volume",
            key="buy_volume",
            value=1.0,
            min_value=0.0,
            format="%.1f",
            step=1.0,
        )

    with col2:
        currency = st.text_input(
            "Security Currency", key="buy_currency", value=default_currency
        )

        buy_date = st.date_input(
            "Date (YYYY-MM-DD)",
            value=date.today(),
            key="buy_date",
            format="YYYY-MM-DD",
        )

    if st.button("📥 Buy Security", key="buy_button", width="stretch"):
        try:
            st.session_state.portfolio.buy_security(
                ticker=ticker_input_buy,
                volume=volume_buy,
                date=buy_date.strftime("%Y-%m-%d"),
                currency=currency,
            )
            st.success(
                f"Bought {volume_buy} unit(s) of {ticker_input_buy} on {buy_date}"
            )

            # Call update_prices to fetch name and price
            market_service.update_prices(st.session_state.portfolio)

            st.rerun()
        except Exception as e:
            st.error(f"Error buying security: {str(e)}")


def _render_sell_box(ticker_options):

    sell_col1, sell_col2 = st.columns(2)
    with sell_col1:
        tickers = st.selectbox(
            "Security ticker",
            options=ticker_options,
            key="ticker_sell_choice",
            index=1 if len(ticker_options) > 1 else 0,
            accept_new_options=True,
        )
        volumes = st.number_input(
            "Volume",
            key="sell_volume",
            value=1.0,
            min_value=0.0,
            format="%.1f",
            step=1.0,
        )

    with sell_col2:
        sell_date = st.date_input(
            "Date (YYYY-MM-DD)",
            value=date.today(),
            key="sell_date",
            format="YYYY-MM-DD",
        )

    if st.button("📤 Sell Security", key="sell_button", width="stretch"):
        try:
            st.session_state.portfolio.sell_security(
                ticker=tickers,
                volume=volumes,
                date=sell_date.strftime("%Y-%m-%d"),
            )
            st.success(f"Sold {volumes} unit(s) of {tickers}")
            st.rerun()  # Global rerun to update table
        except Exception as e:
            st.error(f"Error selling security: {str(e)}")


def _render_save_box(file_list):
    save_filename = st.selectbox(
        "Save as filename",
        options=file_list,
        key="portfolio_file_save",
        index=1 if len(file_list) > 1 and "investment_example.json" in file_list else 0,
        accept_new_options=True,
    )

    if st.button("💾 Save Portfolio", key="save_button", width="stretch"):
        try:
            repo.save_to_json(
                st.session_state.portfolio, PORTFOLIOS_DIR / save_filename
            )
            st.success(f"Portfolio saved to {PORTFOLIOS_DIR / save_filename}")
        except Exception as e:
            st.error(str(e))
