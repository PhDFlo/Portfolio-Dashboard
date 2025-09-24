import streamlit as st
from foliotrack import Currency
from foliotrack import Equilibrate
from foliotrack import Portfolio
from foliotrack import Security

a = Security("AAPL", 100)

# Set up the Streamlit app
st.title("Portfolio Dashboard")

# Placeholder for the main dashboard content
st.write("Welcome to the Portfolio Dashboard!")

# Feature to compare securities given a ticker name and plot their evolution
st.header("Compare Securities")

ticker = st.text_input("Enter ticker name:")
if ticker:
    st.write(f"Plotting evolution for {ticker}")
    # Placeholder for plotting logic
    st.line_chart([1, 2, 3, 4, 5])

# Feature to create a portfolio of ETFs and save it
st.header("Create Portfolio")

etfs = st.text_input("Enter ETF tickers separated by commas:")
if etfs:
    etf_list = etfs.split(",")
    st.write(f"Creating portfolio with ETFs: {etf_list}")
    # Placeholder for saving logic
    st.success("Portfolio saved!")

# Feature to plot the evolution of the portfolio over time
st.header("Plot Portfolio Evolution")

if st.button("Plot Portfolio"):
    st.write("Plotting evolution of the portfolio over time")
    # Placeholder for plotting logic
    st.line_chart([1, 2, 3, 4, 5])
