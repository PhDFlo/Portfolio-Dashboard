import streamlit as st
import numpy as np
import plotly.graph_objects as go
from dashboard.security_comparator import (
    simulate_contract,
    compute_after_tax_curve,
    create_contract_form,
)

st.subheader("Compare Securities")

st.sidebar.header("Contract Details")
years = st.sidebar.number_input("Number of Years", value=30, min_value=1)

contracts = []

col1, col2 = st.columns(2)
with col1:
    contracts.append(
        create_contract_form(
            st,
            "A",
            default_label="PEA",
            default_annual_return=0.06,
            default_capgains_tax=0.172,
        )
    )

with col2:
    contracts.append(
        create_contract_form(
            st,
            "B",
            default_label="CTO",
            default_annual_return=0.08,
            default_capgains_tax=0.30,
        )
    )

if st.button("Compare"):
    series_list = []
    invested_list = []
    after_tax_curves = []
    labels = []
    for contract in contracts:
        series, invested = simulate_contract(
            initial=contract["initial"],
            annual_return=contract["annual_return"],
            years=years,
            security_fee=contract["security_fee"],
            bank_fee=contract["bank_fee"],
            yearly_contribution=contract["yearly_investment"],
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

    # Print last value of each series in the console for debugging
    for idx, (series, label) in enumerate(zip(series_list, labels)):
        st.markdown(f"Final value of {label} (pre-withdrawal): {series[-1]:.2f} €")
        st.markdown(
            f"Final value of {label} (after-tax): {after_tax_curves[idx][-1]:.2f} €"
        )

# Display the plot if it exists in session state
if "comparison_plot" in st.session_state:
    st.plotly_chart(
        st.session_state["comparison_plot"], key="persistent_comparison_plot"
    )
