import streamlit as st
from foliotrack.Equilibrate import solve_equilibrium
import pandas as pd
import datetime
import os
from dashboard.utils_load import update_portfolio_from_dataframe

# Optimization parameters
st.subheader("Optimization")
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
        update_portfolio_from_dataframe(st.session_state.edited_df)
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
        st.session_state.equilibrium_df = pd.DataFrame(equilibrium_data)

    except Exception as e:
        st.error(f"Error during optimization: {str(e)}")


if "equilibrium_df" in st.session_state:
    st.dataframe(
        st.session_state.equilibrium_df,
        use_container_width=True,
        column_config={
            "Price": st.column_config.NumberColumn("Price", format="%.4f"),
            "Target Share": st.column_config.NumberColumn(
                "Target Share", format="%.4f"
            ),
            "Actual Share": st.column_config.NumberColumn(
                "Actual Share", format="%.4f"
            ),
            "Final Share": st.column_config.NumberColumn("Final Share", format="%.4f"),
            "Amount to Invest": st.column_config.NumberColumn(
                "Amount to Invest", format="%.2f"
            ),
            "Number to buy": st.column_config.NumberColumn(
                "Number to buy", format="%.0f"
            ),
        },
    )

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
            st.success(f"Bought {quantity} unit(s) of {ticker_input} at {buy_price}")
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
