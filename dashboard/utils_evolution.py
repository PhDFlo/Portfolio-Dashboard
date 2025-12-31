import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from foliotrack.domain.Portfolio import Portfolio

# Set pandas option to avoid future warnings
pd.set_option("future.no_silent_downcasting", True)

# Define color palette
colors = px.colors.qualitative.Plotly


def get_security_historical_data(tickers: list[str], start_date: str, interval="1d"):
    """Fetch historical market data for all tickers using yfinance and forward fill missing data."""
    stock = yf.Tickers(tickers)

    hist = stock.history(start=start_date, period="max", interval=interval)

    # Fill missing data with values from previous dates
    hist.ffill(inplace=True)
    return hist


def _get_portfolio_history(
    portfolio: Portfolio,
    ticker_list: list[str],
    hist_tickers: pd.DataFrame,
    Date: pd.DatetimeIndex,
) -> pd.DataFrame:
    # Initialize dataframe to track portfolio composition over time
    portfolio_comp = pd.DataFrame(
        columns=[f"Volume {t}" for t in ticker_list]
        + [f"Var {t}" for t in ticker_list]
        + ["Open", "Low", "High", "Close"],
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

    # Verify that all volumes are filled
    for ticker in ticker_list:
        portfolio_comp.loc[portfolio_comp.index[-1], f"Volume {ticker}"] = count_volume[
            ticker
        ]

        # Fill volume between events
        portfolio_comp[f"Volume {ticker}"] = portfolio_comp[f"Volume {ticker}"].ffill(
            axis=0
        )

        # Fill volume remaining NaN with 0
        portfolio_comp[f"Volume {ticker}"] = portfolio_comp[f"Volume {ticker}"].fillna(
            0
        )

    # Compute total value
    for i, date in enumerate(Date):
        # Compute portfolio values
        total_value = {"Open": 0, "Low": 0, "High": 0, "Close": 0}
        for ticker in ticker_list:
            vol = portfolio_comp.loc[date, f"Volume {ticker}"]
            open = hist_tickers.loc[date, ("Open", ticker)]
            low = hist_tickers.loc[date, ("Low", ticker)]
            high = hist_tickers.loc[date, ("High", ticker)]
            close = hist_tickers.loc[date, ("Close", ticker)]

            # Low and high porfolio prices are estimated as the sum of min and max of each security.
            # This is exagerated as min and max values may not occur at the same time during the day.
            total_value["Open"] += vol * open
            total_value["Low"] += vol * low
            total_value["High"] += vol * high
            total_value["Close"] += vol * close

        portfolio_comp.loc[date, "Open"] = total_value["Open"]
        portfolio_comp.loc[date, "Low"] = total_value["Low"]
        portfolio_comp.loc[date, "High"] = total_value["High"]
        portfolio_comp.loc[date, "Close"] = total_value["Close"]

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
        go.Pie(
            labels=ticker_list,
            values=df.target,
            name="Target",
            marker={"colors": colors},
            sort=False,
        ),
        1,
        1,
    )
    fig.add_trace(
        go.Pie(
            labels=ticker_list,
            values=df.actual,
            name="Actual",
            marker={"colors": colors},
            sort=False,
        ),
        2,
        1,
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
        showlegend=False,
    )
    st.plotly_chart(fig)


def plot_portfolio_evolution(
    portfolio: Portfolio,
    ticker_list: list[str],
    hist_tickers: pd.DataFrame,
    Date: pd.DatetimeIndex,
    min_y_exchange: float,
    max_y_exchange: float,
):
    # Get portfolio composition over time
    portfolio_comp = _get_portfolio_history(portfolio, ticker_list, hist_tickers, Date)

    # Create subplot with portfolio value evolution and stacked bar chart of bought/sold volumes
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.25)

    fig.add_trace(
        go.Candlestick(
            x=portfolio_comp.index,
            open=portfolio_comp["Open"],
            high=portfolio_comp["High"],
            low=portfolio_comp["Low"],
            close=portfolio_comp["Close"],
            name="Portfolio value",
        ),
        row=1,
        col=1,
    )

    # Create stacked bar chart of bought and sold volumes over time
    for ticker in ticker_list:
        fig.add_trace(
            go.Bar(
                x=portfolio_comp.index,
                y=portfolio_comp[f"Var {ticker}"],
                name=ticker,
                hoverinfo="x+name+y",
                marker={
                    "color": colors[ticker_list.index(ticker)],
                    "line": {"width": 3.0, "color": colors[ticker_list.index(ticker)]},
                },
            ),
            row=2,
            col=1,
        )

    fig.update_layout(
        height=800,
        title_text="Portfolio Time Evolution",
        yaxis_title=f"Portfolio Value ({st.session_state.portfolio.symbol})",
        yaxis2_title="Security Volumes Exchanges, Buy (+) / Sell (-)",
        yaxis=dict(domain=[0.4, 1.0]),
        yaxis2=dict(domain=[0.0, 0.2]),
    )

    # Set y-axis range
    fig["layout"]["yaxis"].update(range=[0, max(portfolio_comp["High"])])
    fig["layout"]["yaxis2"].update(range=[min_y_exchange, max_y_exchange])

    # Display stacked bar chart of security volumes over time
    st.plotly_chart(fig)
