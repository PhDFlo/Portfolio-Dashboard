import streamlit as st
from dashboard import (
    side_bar_file_operations,
)
from foliotrack.Portfolio import Portfolio
import pandas as pd

# For test
from numpy.random import default_rng as rng
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Side bar for file operations
side_bar_file_operations()

# Display current portfolio in editable table
if "portfolio" not in st.session_state:
    # Ensure a portfolio object exists in session state for pages run standalone
    st.session_state.portfolio = Portfolio()

col1, col2 = st.columns([3, 1])

with col1:
    hist_data = [
        rng(0).standard_normal(200) - 2,
        rng(1).standard_normal(200),
        rng(2).standard_normal(200) + 2,
    ]
    group_labels = ["Group 1", "Group 2", "Group 3"]

    fig = ff.create_distplot(hist_data, group_labels, bin_size=[0.1, 0.25, 0.5])

    st.plotly_chart(fig)

with col2:
    ticker_list = [ticker for ticker in st.session_state.portfolio.securities]
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
