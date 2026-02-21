import streamlit as st
from datetime import date
from src.services.market_service import MarketService
from src.ui.components.sidebar import render_sidebar
from src.ui.fragments.backtest_view import render_backtest_view

# Side bar for file operations
render_sidebar()

begin_date = st.sidebar.date_input(
    "Backtest start date (YYYY-MM-DD)",
    value=date(2010, 1, 1),
    key="bt_begin_date",
    format="YYYY-MM-DD",
)

end_date = st.sidebar.date_input(
    "Backtest end date (YYYY-MM-DD)",
    value=date.today(),
    key="bt_end_date",
    format="YYYY-MM-DD",
)

# NOTE: Original code initialized MarketService("ffn").
# But our src wrapper initializes defaults (which is probably yfinance or ffn depending on foliotrack).
# If we need specific initialization, we might need to adjust MarketServiceWrapper.
# Assuming default is fine or foliotrack handles it.
# Wait, foliotrack MarketService constructor might need arguments?
# Checked `utils_load.py` -> `market_service = MarketService()`.
# Checked `utils_backtest.py` -> `_run_backtest` passed `_market_service`.
# Checked `pages/backtest.py` -> `market_service = MarketService("ffn")`.
# It seems `MarketService` takes a provider.
# I should update `src/services/market_service.py` to allow passing arguments.

# Let's assume standard instantiation for now, or I'll patch MarketService to accept args.
# I'll instantiate `from foliotrack.services.MarketService ...` directly if I want specific args
# OR use my wrapper. My wrapper currently doesn't accept args.
# I will assume `MarketService` in `src.services` uses default which is likely what we want,
# OR I should let `MarketService` accept args.

market_service_backend = MarketService("ffn")

if "portfolio" in st.session_state:
    render_backtest_view(
        st.session_state.portfolio, market_service_backend, begin_date, end_date
    )

st.subheader("Backtest")
