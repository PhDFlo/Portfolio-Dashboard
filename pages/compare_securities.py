import streamlit as st
import numpy as np
import plotly.graph_objects as go
from dashboard.security_comparator import (
    simulate_contract,
    compute_after_tax_curve,
    parse_contract_arg,
)

st.subheader("Compare Securities")

st.sidebar.header("Contract Details")
initial = st.sidebar.number_input("Initial Investment", value=10000.0)
annual_return = st.sidebar.number_input("Annual Return (e.g. 0.06 for 6%)", value=0.06)
years = st.sidebar.number_input("Number of Years", value=30, min_value=1)
yearly_contribution = st.sidebar.number_input("Yearly Contribution", value=0.0)

contracts = []

col1, col2 = st.columns(2)
with col1:
    st.subheader("Contract 1")
    label = st.text_input("Label 1", value="Contract 1")
    security_fee = st.number_input("Security Fee 1 (e.g. 0.005 for 0.5%)", value=0.005)
    bank_fee = st.number_input("Bank Fee 1 (e.g. 0.005 for 0.5%)", value=0.005)
    capgains_tax = st.number_input(
        "Capital Gains Tax 1 (e.g. 0.30 for 30%)", value=0.30
    )
    contracts.append(f"{label},{security_fee},{bank_fee},{capgains_tax}")
with col2:
    st.subheader("Contract 2")
    label = st.text_input("Label 2", value="Contract 2")
    security_fee = st.number_input("Security Fee 2 (e.g. 0.005 for 0.5%)", value=0.005)
    bank_fee = st.number_input("Bank Fee 2 (e.g. 0.005 for 0.5%)", value=0.005)
    capgains_tax = st.number_input(
        "Capital Gains Tax 2 (e.g. 0.30 for 30%)", value=0.30
    )
    contracts.append(f"{label},{security_fee},{bank_fee},{capgains_tax}")

if st.button("Compare"):
    series_list = []
    invested_list = []
    after_tax_curves = []
    labels = []
    for contract_str in contracts:
        contract = parse_contract_arg(contract_str)
        series, invested = simulate_contract(
            initial=initial,
            annual_return=annual_return,
            years=years,
            security_fee=contract["security_fee"],
            bank_fee=contract["bank_fee"],
            yearly_contribution=yearly_contribution,
        )
        after_tax_curve = compute_after_tax_curve(
            series, invested, contract["capgains_tax"]
        )
        series_list.append(series)
        invested_list.append(invested)
        after_tax_curves.append(after_tax_curve)
        labels.append(contract["label"])

    xs = np.arange(0, years + 1)
    fig = go.Figure()
    colors = [
        "blue",
        "green",
        "red",
        "purple",
        "orange",
        "brown",
        "pink",
        "gray",
        "olive",
        "cyan",
    ]
    for idx, (series, after_tax_curve, label) in enumerate(
        zip(series_list, after_tax_curves, labels)
    ):
        color = colors[idx % len(colors)]
        fig.add_trace(
            go.Scatter(
                x=xs,
                y=series,
                mode="lines",
                name=f"{label} (pre-withdrawal)",
                line=dict(color=color, dash="dash"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=xs,
                y=after_tax_curve,
                mode="lines",
                name=f"{label} (after-tax)",
                line=dict(color=color),
            )
        )
    fig.update_layout(
        title="Security investment comparison (fees & capital gains tax)",
        xaxis_title="Years",
        yaxis_title="Portfolio value",
        legend_title="Contracts",
    )

    # Store the plot in session state to persist across pages
    st.session_state["comparison_plot"] = fig

# Display the plot if it exists in session state
if "comparison_plot" in st.session_state:
    st.plotly_chart(
        st.session_state["comparison_plot"], key="persistent_comparison_plot"
    )
