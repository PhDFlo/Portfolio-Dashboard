import streamlit as st
import numpy as np
import plotly.graph_objects as go
from dashboard.utils_sec_comp import (
    simulate_contract,
    compute_after_tax_curve,
    create_contract_form,
    plotly_colors,
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
            label="PEA",
            annual_return=0.06,
            capgains_tax=0.172,
            years=years,
        )
    )

with col2:
    contracts.append(
        create_contract_form(
            st,
            "B",
            label="CTO",
            annual_return=0.08,
            capgains_tax=0.30,
            years=years,
        )
    )

if st.button("Compare"):
    series_list = []
    invested_list = []
    after_tax_curves = []
    labels = []
    for contract in contracts:
        series, invested = simulate_contract(contract)
        after_tax_curve = compute_after_tax_curve(
            series, invested, contract["capgains_tax"]
        )
        series_list.append(series)
        invested_list.append(invested)
        after_tax_curves.append(after_tax_curve)
        labels.append(contract["label"])

    xs = np.arange(0, years + 1)
    fig = go.Figure()
    for idx, (series, after_tax_curve, label) in enumerate(
        zip(series_list, after_tax_curves, labels)
    ):
        fig.add_trace(
            go.Scatter(
                x=xs,
                y=series,
                mode="lines",
                name=f"{label} (pre-withdrawal)",
                line=dict(color=plotly_colors[idx], dash="dash"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=xs,
                y=after_tax_curve,
                mode="lines",
                name=f"{label} (after-tax)",
                line=dict(color=plotly_colors[idx], dash="solid"),
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
