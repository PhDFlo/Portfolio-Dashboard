import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from foliotrack.Portfolio import Portfolio

# Set pandas option to avoid future warnings
pd.set_option("future.no_silent_downcasting", True)


def _get_security_historical_data(tickers: list[str], start_date: str, interval="1d"):
    """Fetch historical market data for all tickers using yfinance and forward fill missing data."""
    stock = yf.Tickers(tickers)

    hist = stock.history(start=start_date, period="max", interval=interval)

    # Fill missing data with values from previous dates
    hist.ffill(inplace=True)
    return hist


def _get_portfolio_history(
    portfolio: Portfolio,
    ticker_list: list[str],
    Date: pd.DatetimeIndex,
) -> pd.DataFrame:
    # Initialize dataframe to track portfolio composition over time
    portfolio_comp = pd.DataFrame(
        columns=[f"Volume {t}" for t in ticker_list]
        + [f"Var {t}" for t in ticker_list]
        + ["Value"],
        index=Date,
    )

    # Initialize volume tracker
    count_volume = {ticker: 0 for ticker in ticker_list}

    for event in portfolio.history:
        ticker = event["ticker"]
        volume = event["volume"]
        date = event["date"]

        # Add or remove volume based on action
        count_volume[ticker] += volume
        portfolio_comp.loc[date, f"Volume {ticker}"] = count_volume[ticker]
        portfolio_comp.loc[date, f"Var {ticker}"] = volume

        # Fill volume between events
        portfolio_comp[f"Volume {ticker}"] = portfolio_comp[f"Volume {ticker}"].ffill()

    # Fill any remaining NaN with 0
    portfolio_comp.fillna(0, inplace=True)

    return portfolio_comp


def plot_pie_chart(portfolio: Portfolio, ticker_list: list[str]):
    df = pd.DataFrame(columns=("target", "actual", "final"), index=ticker_list)

    for security in portfolio.securities:
        shares = portfolio._get_share(security)
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
    fig.update_layout(
        title_text="Target vs Actual Security Shares",
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
        # template="plotly",
    )
    st.plotly_chart(fig)


def plot_portfolio_evolution(
    portfolio: Portfolio,
    ticker_list: list[str],
    start_date: str,
):
    # Get historical data for all tickers in portfolio
    hist_tickers = _get_security_historical_data(
        ticker_list, start_date=start_date, interval="1d"
    )
    Date = hist_tickers.index

    # Get portfolio composition over time
    portfolio_comp = _get_portfolio_history(portfolio, ticker_list, Date)

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

    fig_evol = px.line(
        portfolio_comp,
        x=portfolio_comp.index,
        y="Value",
        title="Portfolio Value Evolution",
        labels={
            "Date": "",
            "Value": f"Portfolio Value ({portfolio.currency})",
        },
    )

    # Display line chart of portfolio value over time
    st.plotly_chart(fig_evol)

    # Create stacked bar chart of bought and sold volumes over time
    go_data = []
    for ticker in ticker_list:
        go_data.append(
            go.Bar(
                x=portfolio_comp.index,
                y=portfolio_comp[f"Var {ticker}"],
                name=ticker,
                hoverinfo="x+name+y",
            )
        )

    fig_bar = go.Figure(data=go_data)
    fig_bar.update_layout(
        xaxis_title_text="",  # xaxis label
        yaxis_title_text="Volume acquired or sold",  # yaxis label
        bargap=0.2,  # gap between bars of adjacent location coordinates
        bargroupgap=0.1,  # gap between bars of the same location coordinates
    )

    # Display stacked bar chart of security volumes over time
    st.plotly_chart(fig_bar)
