import streamlit as st
from datetime import datetime
from foliotrack import get_rate_between, Currency

# Get list of currency codes
c = Currency()
currencies = c._currency_data
currency_codes = [d["name"] + " (" + d["symbol"] + ")" for d in currencies]

st.subheader("Exchange Rates")

# Sidebar input
date_str = st.sidebar.date_input("Date (YYYY-MM-DD) — optional", format="YYYY-MM-DD")

col1, col2 = st.columns(2)
with col1:
    from_currency = st.selectbox(
        "From currency (ISO code)",
        options=currency_codes,
        key="from_currency_select",
        index=currency_codes.index("European Euro (€)")
        if "European Euro (€)" in currency_codes
        else 0,
    )
with col2:
    to_currency = st.selectbox(
        "To currency (ISO code)",
        options=currency_codes,
        key="to_currency_select",
        index=currency_codes.index("United States dollar ($)")
        if "United States dollar ($)" in currency_codes
        else 0,
    )
amount = st.number_input("Amount", value=1.0, min_value=0.0, format="%f")


# Replace normalization of selected labels with mapping back to currency codes
from_idx = (
    currency_codes.index(from_currency) if from_currency in currency_codes else None
)
from_currency_code = currencies[from_idx].get("cc")
to_idx = currency_codes.index(to_currency) if to_currency in currency_codes else None
to_currency_code = currencies[to_idx].get("cc")


# Use resolved codes when calling the API
if st.button("⚖️ Get rate", use_container_width=True):
    if not from_currency or not to_currency:
        st.error("Please provide both from and to currency ISO codes.")
    else:
        try:
            result = get_rate_between(
                from_currency_code, to_currency_code, date=str(date_str)
            )
        except Exception as e:
            st.error(f"Error fetching exchange rate: {e}")
        else:
            # Try to display common result shapes
            if isinstance(result, dict):
                # Common keys: 'rate', 'converted', 'from', 'to'
                rate = result.get("rate")
                converted = result.get("converted")
                if rate is not None:
                    st.markdown(
                        f"Exchange rate {from_currency_code} → {to_currency_code}: **{rate}**"
                    )
                if converted is not None:
                    st.markdown(f"Converted amount: **{converted}** {to_currency_code}")
                st.write(result)
            elif isinstance(result, (int, float)):
                st.markdown(
                    f"Exchange rate {from_currency_code} → {to_currency_code}: **{result}**"
                )
                st.markdown(
                    f"Converted amount: **{result * amount}** {to_currency_code}"
                )
            else:
                # Generic display if the return type is different
                st.write(result)
