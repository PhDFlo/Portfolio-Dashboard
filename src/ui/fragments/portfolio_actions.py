import streamlit as st
from foliotrack.services.MarketService import MarketService
from foliotrack.storage.PortfolioRepository import PortfolioRepository

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
        default_buy_price = 0.0
        if (
            len(st.session_state.portfolio.securities) != 0
            and ticker_input_buy in st.session_state.portfolio.securities
        ):
            default_currency = st.session_state.portfolio.securities[
                ticker_input_buy
            ].currency
            default_buy_price = st.session_state.portfolio.securities[
                ticker_input_buy
            ].price_in_security_currency

        volume_buy = st.number_input(
            "Volume to Buy",
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

        buy_price = st.number_input(
            "Unit Price",
            key="buy_price",
            value=default_buy_price,
            min_value=0.0,
            format="%.2f",
        )

    if st.button("📥 Buy Security", key="buy_button", width="stretch"):
        try:
            st.session_state.portfolio.buy_security(
                ticker=ticker_input_buy,
                volume=volume_buy,
                price=buy_price,
                currency=currency,
            )
            st.success(
                f"Bought {volume_buy} unit(s) of {ticker_input_buy} at {buy_price}"
            )

            # Call update_prices to fetch name and price
            market_service.update_prices(st.session_state.portfolio)

            st.rerun()
        except Exception as e:
            st.error(f"Error buying security: {str(e)}")


def _render_sell_box(ticker_options):
    tickers = st.selectbox(
        "Security ticker to sell",
        options=ticker_options,
        key="ticker_sell_choice",
        index=1 if len(ticker_options) > 1 else 0,
        accept_new_options=True,
    )
    volumes = st.number_input(
        "Volume to Sell",
        key="sell_volume",
        value=1.0,
        min_value=0.0,
        format="%.1f",
        step=1.0,
    )

    if st.button("📤 Sell Security", key="sell_button", width="stretch"):
        try:
            st.session_state.portfolio.sell_security(
                ticker=tickers,
                volume=volumes,
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
            path = repo.save_to_json(st.session_state.portfolio, save_filename)
            st.success(f"Portfolio saved to {path}")
        except Exception as e:
            st.error(str(e))
