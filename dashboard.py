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
st.title("📈 Portfolio Dashboard")

# Initialize session state for portfolio
if "portfolio" not in st.session_state:
    st.session_state.portfolio = Portfolio()

load = st.Page(
    "pages/load_portfolio.py",
    title="Portfolio & Update Prices",
    icon="📂",
)

equil = st.Page(
    "pages/equilibrium_buy.py",
    title="Equilibrium, Buy & Export",
    icon="🔨",
)

compare = st.Page(
    "pages/compare_securities.py",
    title="Compare Securities",
    icon="📚",
)

pg = st.navigation(
    {
        "Manage": [
            load,
            equil,
        ],
        "Tools": [
            compare,
        ],
    }
)

# Run pages
pg.run()


# Footer
st.markdown("---")
st.markdown("**Security Portfolio Optimizer** - Built with foliotrack and Streamlit")
