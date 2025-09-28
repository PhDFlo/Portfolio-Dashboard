import streamlit as st
from foliotrack.Portfolio import Portfolio
from pages.utils import get_portfolio_files, load_portfolio_from_file
import os

# Configure page
st.set_page_config(
    page_title="Security Portfolio Optimizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state for portfolio
if "portfolio" not in st.session_state:
    st.session_state.portfolio = Portfolio()


# Main app
st.title("📊 Security Portfolio Optimizer")

# Sidebar for file operations
with st.sidebar:
    st.header("Portfolio Files")

    # File selection
    portfolio_files = get_portfolio_files()
    file_options = [""] + [os.path.basename(f) for f in portfolio_files]

    selected_file = st.selectbox(
        "Select Portfolio JSON",
        options=file_options,
        index=1
        if len(file_options) > 1 and "investment_example.json" in file_options
        else 0,
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh Files"):
            st.rerun()

    with col2:
        if st.button("📂 Load Portfolio") and selected_file:
            load_portfolio_from_file(f"./Portfolios/{selected_file}")
            st.rerun()

# Create tabs
tab1, tab2 = st.tabs(["📈 Portfolio & Update Prices", "⚖️ Equilibrium, Buy & Export"])

# Footer
st.markdown("---")
st.markdown("**Security Portfolio Optimizer** - Built with Streamlit and foliotrack")
