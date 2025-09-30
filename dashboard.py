import streamlit as st
from foliotrack.Portfolio import Portfolio

# Configure page
st.set_page_config(
    page_title="Security Portfolio Optimizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Main app
st.title("📊 Security Portfolio Optimizer")

# Initialize session state for portfolio
if "portfolio" not in st.session_state:
    st.session_state.portfolio = Portfolio()

load = st.Page(
    "pages/load_portfolio.py",
    title="Portfolio & Update Prices",
    icon="📈",
)

equil = st.Page(
    "pages/equilibrium_buy.py",
    title="Equilibrium, Buy & Export",
    icon="⚖️",
)

pg = st.navigation(
    {
        "Manage": [
            load,
            equil,
        ],
        "Tools": [],
    }
)

# Run pages
pg.run()


# Footer
st.markdown("---")
st.markdown("**Security Portfolio Optimizer** - Built with foliotrack and Streamlit")
