import streamlit as st
from foliotrack.Security import Security
from foliotrack.Portfolio import Portfolio
from foliotrack.Equilibrate import solve_equilibrium
import pandas as pd
import datetime
import os
import glob

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


def get_portfolio_files():
    """Get list of JSON files in Portfolios directory"""
    if not os.path.exists("./Portfolios"):
        os.makedirs("./Portfolios", exist_ok=True)
    return glob.glob("./Portfolios/*.json")


def load_portfolio_data(portfolio):
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
                "Actual Share": security.get("actual_share"),
                "Target Share": security.get("target_share"),
                f"Amount Invested ({portfolio.symbol})": security.get(
                    "amount_invested"
                ),
                "Number Held": security.get("number_held"),
            }
        )
    return pd.DataFrame(data)


def load_portfolio_from_file(filename):
    """Load portfolio from JSON file"""
    try:
        st.session_state.portfolio = Portfolio.from_json(filename)
        st.success(f"Portfolio loaded from {filename}")
        return True
    except Exception as e:
        st.error(f"Error loading portfolio: {str(e)}")
        return False


def save_portfolio_to_file(filename):
    """Save portfolio to JSON file"""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        st.session_state.portfolio.to_json(filename)
        st.success(f"Portfolio saved to {filename}")
        return True
    except Exception as e:
        st.error(f"Error saving portfolio: {str(e)}")
        return False


def update_portfolio_from_dataframe(df):
    """Update portfolio object from edited dataframe"""
    st.session_state.portfolio.securities.clear()
    for _, row in df.iterrows():
        if pd.notna(row["Name"]) and pd.notna(row["Ticker"]):
            security = Security(
                name=str(row["Name"]),
                ticker=str(row["Ticker"]),
                currency=str(row["Currency"]) if pd.notna(row["Currency"]) else "EUR",
                price_in_security_currency=float(row["Price"])
                if pd.notna(row["Price"])
                else 0.0,
                actual_share=float(row["Actual Share"])
                if pd.notna(row["Actual Share"])
                else 0.0,
                target_share=float(row["Target Share"])
                if pd.notna(row["Target Share"])
                else 0.0,
                number_held=float(row["Number Held"])
                if pd.notna(row["Number Held"])
                else 0.0,
            )
            st.session_state.portfolio.add_security(security)


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

with tab1:
    st.header("Portfolio Management")

    # Display current portfolio in editable table
    if st.session_state.portfolio.securities:
        df = load_portfolio_data(st.session_state.portfolio)
    else:
        # Create empty dataframe with proper structure
        df = pd.DataFrame(
            {
                "Name": [""],
                "Ticker": [""],
                "Currency": ["EUR"],
                "Price": [0.0],
                "Actual Share": [0.0],
                "Target Share": [0.0],
                f"Amount Invested ({st.session_state.portfolio.symbol})": [0.0],
                "Number Held": [0.0],
            }
        )

    st.subheader("Security List")
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Name": st.column_config.TextColumn("Name", width="medium"),
            "Ticker": st.column_config.TextColumn("Ticker", width="small"),
            "Currency": st.column_config.TextColumn("Currency", width="small"),
            "Price": st.column_config.NumberColumn("Price", format="%.4f"),
            "Actual Share": st.column_config.NumberColumn(
                "Actual Share", format="%.4f"
            ),
            "Target Share": st.column_config.NumberColumn(
                "Target Share", format="%.4f"
            ),
            f"Amount Invested ({st.session_state.portfolio.symbol})": st.column_config.NumberColumn(
                f"Amount Invested ({st.session_state.portfolio.symbol})", format="%.2f"
            ),
            "Number Held": st.column_config.NumberColumn("Number Held", format="%.0f"),
        },
        key="portfolio_editor",
    )

    # Update portfolio if data was edited
    if not edited_df.equals(df):
        update_portfolio_from_dataframe(edited_df)

    # Action buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("💰 Update Security Prices", use_container_width=True):
            try:
                st.session_state.portfolio.update_security_prices()
                st.session_state.portfolio.compute_actual_shares()
                st.success("Security prices updated!")
                st.rerun()
            except Exception as e:
                st.error(f"Error updating prices: {str(e)}")

    with col2:
        if st.button("🔄 Refresh Portfolio Display", use_container_width=True):
            st.rerun()

    # Save portfolio section
    st.subheader("Save Portfolio")
    col1, col2 = st.columns([3, 1])

    with col1:
        default_filename = (
            f"Portfolios/investment_{datetime.datetime.now().strftime('%d_%m_%Y')}.json"
        )
        save_filename = st.text_input("Save as filename", value=default_filename)

    with col2:
        st.write("")  # Add spacing
        st.write("")  # Add spacing
        if st.button("💾 Save Portfolio"):
            save_portfolio_to_file(save_filename)

with tab2:
    st.header("Portfolio Optimization & Trading")

    # Optimization parameters
    st.subheader("Optimization Parameters")
    col1, col2 = st.columns(2)

    with col1:
        new_investment = st.number_input(
            "New Investment Amount (€)", value=500.0, min_value=0.0, format="%.2f"
        )

    with col2:
        min_percent = st.number_input(
            "Minimum Percentage to Invest",
            value=0.99,
            min_value=0.0,
            max_value=1.0,
            format="%.2f",
        )

    # Optimization button and results
    if st.button("🎯 Optimize Portfolio", use_container_width=True):
        try:
            # Update portfolio from current data
            update_portfolio_from_dataframe(edited_df)
            st.session_state.portfolio.compute_actual_shares()

            # Run optimization
            solve_equilibrium(
                st.session_state.portfolio,
                investment_amount=float(new_investment),
                min_percent_to_invest=float(min_percent),
            )

            # Display results
            info = st.session_state.portfolio.get_portfolio_info()
            equilibrium_data = []
            for security_info in info:
                equilibrium_data.append(
                    {
                        "Name": security_info.get("name"),
                        "Ticker": security_info.get("ticker"),
                        "Currency": security_info.get("currency"),
                        "Price": security_info.get("price_in_security_currency"),
                        "Target Share": security_info.get("target_share"),
                        "Actual Share": security_info.get("actual_share"),
                        "Final Share": security_info.get("final_share"),
                        "Amount to Invest": security_info.get("amount_to_invest"),
                        "Number to buy": security_info.get("number_to_buy"),
                    }
                )

            equilibrium_df = pd.DataFrame(equilibrium_data)

            st.subheader("Equilibrium Portfolio Results")
            st.dataframe(
                equilibrium_df,
                use_container_width=True,
                column_config={
                    "Price": st.column_config.NumberColumn("Price", format="%.4f"),
                    "Target Share": st.column_config.NumberColumn(
                        "Target Share", format="%.4f"
                    ),
                    "Actual Share": st.column_config.NumberColumn(
                        "Actual Share", format="%.4f"
                    ),
                    "Final Share": st.column_config.NumberColumn(
                        "Final Share", format="%.4f"
                    ),
                    "Amount to Invest": st.column_config.NumberColumn(
                        "Amount to Invest", format="%.2f"
                    ),
                    "Number to buy": st.column_config.NumberColumn(
                        "Number to buy", format="%.0f"
                    ),
                },
            )

            # Store equilibrium results in session state
            st.session_state.equilibrium_results = equilibrium_df

        except Exception as e:
            st.error(f"Error during optimization: {str(e)}")

    # Display stored equilibrium results if available
    if "equilibrium_results" in st.session_state:
        st.subheader("Current Equilibrium Results")
        st.dataframe(st.session_state.equilibrium_results, use_container_width=True)

    # Security purchase section
    st.subheader("Buy Security")

    col1, col2, col3 = st.columns(3)

    with col1:
        ticker_input = st.text_input("Security Ticker")
        buy_price = st.number_input("Unit Price", value=0.0, format="%.4f")

    with col2:
        quantity = st.number_input("Quantity to Buy", value=1.0, format="%.4f")
        fee = st.number_input("Transaction Fee (€, $, ...)", value=0.0, format="%.2f")

    with col3:
        purchase_date = st.date_input("Purchase Date", value=datetime.date.today())
        st.write("")  # Add spacing
        if st.button("💸 Buy Security"):
            try:
                st.session_state.portfolio.buy_security(
                    ticker_input,
                    quantity,
                    buy_price=buy_price,
                    date=str(purchase_date),
                    fee=fee,
                )
                st.success(
                    f"Bought {quantity} unit(s) of {ticker_input} at {buy_price}"
                )
            except Exception as e:
                st.error(f"Error buying security: {str(e)}")

    # Export section
    st.subheader("Export Staged Purchases")

    col1, col2 = st.columns([3, 1])

    with col1:
        export_filename = st.text_input(
            "Export filename", value="Purchases/staged_purchases.csv"
        )

    with col2:
        st.write("")  # Add spacing
        st.write("")  # Add spacing
        if st.button("📤 Export Purchases"):
            try:
                # Ensure directory exists
                os.makedirs(os.path.dirname(export_filename), exist_ok=True)
                st.session_state.portfolio.purchases_to_wealthfolio_csv(export_filename)
                st.success(f"Staged purchases exported to {export_filename}")
            except Exception as e:
                st.error(f"Error exporting purchases: {str(e)}")

# Footer
st.markdown("---")
st.markdown("**Security Portfolio Optimizer** - Built with Streamlit and foliotrack")
