import streamlit as st
from dashboard import (
    side_bar_file_operations,
)
from foliotrack.Portfolio import Portfolio
from dashboard.utils_evolution import get_historical_data
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


# Side bar for file operations
side_bar_file_operations()

# Display current portfolio in editable table
if "portfolio" not in st.session_state:
    # Ensure a portfolio object exists in session state for pages run standalone
    st.session_state.portfolio = Portfolio()

ticker_list = [ticker for ticker in st.session_state.portfolio.securities]

col1, col2 = st.columns([3, 1])

# Display portfolio value evolution over time
with col1:
    if ticker_list != []:
        # Get historical data for all tickers in portfolio
        hist_tickers = get_historical_data(
            ticker_list, start_date="2023-02-14", interval="1d"
        )
        # Forward fill missing data
        hist_tickers.ffill(inplace=True)
        Date = hist_tickers.index

        # Initialize dataframe to track portfolio composition over time
        portfolio_comp = pd.DataFrame(
            columns=[f"Volume {t}" for t in ticker_list] + ["Value"], index=Date
        )

        # Track volume of each security over time
        hist_portfolio = st.session_state.portfolio.history

        # Initialize volume tracker
        track_volume = {ticker: 0 for ticker in ticker_list}

        for event in hist_portfolio:
            ticker = event["ticker"]
            volume = event["volume"]
            action = event["action"]
            date = event["date"]

            try:
                price = hist_tickers.loc[date, ("Close", ticker)]
            except KeyError:
                # Skip if date not found in historical data
                continue

            col_name = f"Volume {ticker}"

            # Add or remove volume based on action
            track_volume[ticker] += volume if action == "buy" else -volume
            portfolio_comp.loc[date, col_name] = track_volume[ticker]

        # Fill volume between events
        portfolio_comp.ffill(inplace=True)
        # Fill any remaining NaN with 0
        portfolio_comp.fillna(0, inplace=True)

        # Compute total value
        for date in portfolio_comp.index:
            total_value = 0
            for ticker in ticker_list:
                vol = portfolio_comp.loc[date, f"Volume {ticker}"]
                price = hist_tickers.loc[date, ("Close", ticker)]
                total_value += vol * price
            portfolio_comp.loc[date, "Value"] = total_value

    fig = px.line(
        portfolio_comp,
        x=portfolio_comp.index,
        y="Value",
        title="Portfolio Value Evolution",
        labels={
            "Date": "",
            "Value": f"Portfolio Value ({st.session_state.portfolio.currency})",
        },
    )

    st.plotly_chart(fig)

# Display target vs actual shares in donut charts
with col2:
    df = pd.DataFrame(columns=("target", "actual", "final"), index=ticker_list)

    for security in st.session_state.portfolio.securities:
        shares = st.session_state.portfolio._get_share(security)
        df.loc[security] = [
            shares.target,
            shares.actual,
            shares.final,
        ]

    # Create subplots: use 'domain' type for Pie subplot
    fig = make_subplots(
        rows=2, cols=1, specs=[[{"type": "domain"}], [{"type": "domain"}]]
    )
    fig.add_trace(
        go.Pie(labels=ticker_list, values=df.target, name="Target", sort=False), 1, 1
    )
    fig.add_trace(
        go.Pie(labels=ticker_list, values=df.actual, name="Actual", sort=False), 2, 1
    )

    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=0.4, hoverinfo="label+percent+name")
    fig.update_layout(template="plotly")
    fig.update_layout(
        title_text="Portfolio Target vs Actual Security Shares",
        height=700,
        # Add annotations in the center of the donut pies.
        annotations=[
            dict(
                text="Target",
                x=0.5,
                y=sum(fig.get_subplot(1, 1).y) / 2,
                font_size=20,
                showarrow=False,
                yanchor="middle",
            ),
            dict(
                text="Actual",
                x=0.5,
                y=sum(fig.get_subplot(2, 1).y) / 2,
                font_size=20,
                showarrow=False,
                yanchor="middle",
            ),
        ],
    )
    st.plotly_chart(fig)
