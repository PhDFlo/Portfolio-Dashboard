import numpy as np

plotly_colors = [
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


def simulate_contract(contract):
    """
    Simulate yearly portfolio value after applying gross return, Security fee and bank fee.

    Parameters:
        contract (dict): a dictionary containing the contract parameters:
            - initial (float): initial investment
            - annual_return (float): annual return (as a decimal, e.g. 0.07 for 7%)
            - security_fee (float): annual security fee (as a decimal)
            - bank_fee (float): annual bank fee (as a decimal)
            - yearly_investment (float): yearly investment added at the end of each year
            - years (int): number of years to simulate

    Returns:
        tuple: (values_by_year, total_invested)
            values_by_year (numpy array): portfolio values at each year
            total_invested (float): total amount invested
    """

    # Initialize array to store values at each year
    values = np.empty(contract["years"] + 1)
    values[0] = contract["initial"]
    # Initialize total invested
    invested = contract["initial"]
    # Simulate yearly portfolio value
    for y in range(1, contract["years"] + 1):
        # Apply gross return
        val = values[y - 1] * (1.0 + contract["annual_return"])
        # Apply security expense ratio (reduces return)
        val *= 1.0 - contract["security_fee"]
        # Apply bank annual fee (as % of assets at year end)
        val *= 1.0 - contract["bank_fee"]
        # Add yearly contribution at year end (after fees)
        if contract["yearly_investment"]:
            val += contract["yearly_investment"]
            invested += contract["yearly_investment"]
        # Store value at this year
        values[y] = val
    return values, invested


def compute_after_tax_curve(values, invested, capital_gains_tax):
    """
    Compute after-tax portfolio value at each year, as if liquidated at that year.

    Parameters:
        values (numpy array): portfolio values at each year
        invested (float): total amount invested
        capital_gains_tax (float): capital gains tax rate

    Returns:
        numpy array: after-tax values (same length as values)
    """
    # Compute gains
    gains = np.maximum(0.0, values - invested)
    # Compute taxes
    taxes = gains * capital_gains_tax
    # Compute after-tax values
    after_tax = values - taxes
    return after_tax


def create_contract_form(
    st,
    key_prefix,
    label="Contract",
    initial=10000.0,
    annual_return=0.06,
    yearly_investment=0.0,
    security_fee=0.005,
    bank_fee=0.005,
    capgains_tax=0.3,
    years=30,
):
    """
    Create a contract form in the Streamlit app with default values and labels.

    Parameters:
        st (Streamlit): the Streamlit app object
        key_prefix (str): prefix for the form field keys
        label (str): default label for the contract
        initial (float): default initial investment
        annual_return (float): default annual return
        yearly_investment (float): default yearly investment
        security_fee (float): default security fee
        bank_fee (float): default bank fee
        capgains_tax (float): default capital gains tax
        years (int): default number of years

    Returns:
        contract (dict): a dictionary containing the contract form values
    """
    st.subheader(f"Contract {key_prefix.upper()}")
    label = st.text_input(
        "Label",
        value=f"{label}",
        key=f"label_{key_prefix}",
    )
    initial = st.number_input(
        f"Initial Investment (e.g. {initial}€)",
        value=initial,
        format="%.2f",
        key=f"initial_{key_prefix}",
    )
    annual_return = st.number_input(
        f"Annual Return (e.g. {annual_return} for {annual_return * 100}%)",
        value=annual_return,
        format="%.3f",
        min_value=0.0,
        max_value=1.0,
        key=f"annual_return_{key_prefix}",
    )
    yearly_investment = st.number_input(
        f"Yearly Investment (e.g. {yearly_investment}€) ",
        value=yearly_investment,
        format="%.2f",
        key=f"yearly_investment_{key_prefix}",
    )
    security_fee = st.number_input(
        f"Annual Security Fee (e.g. {security_fee} for {security_fee * 100}%)",
        value=security_fee,
        format="%.3f",
        min_value=0.0,
        max_value=1.0,
        key=f"security_fee_{key_prefix}",
    )
    bank_fee = st.number_input(
        f"Annual Bank Fee (e.g. {bank_fee} for {bank_fee * 100}%)",
        value=bank_fee,
        format="%.3f",
        min_value=0.0,
        max_value=1.0,
        key=f"bank_fee_{key_prefix}",
    )
    capgains_tax = st.number_input(
        f"Capital Gains Tax (e.g. {capgains_tax} for {capgains_tax * 100}%)",
        value=capgains_tax,
        format="%.3f",
        min_value=0.0,
        max_value=1.0,
        key=f"capgains_tax_{key_prefix}",
    )
    contract = {
        "label": label,
        "initial": initial,
        "annual_return": annual_return,
        "yearly_investment": yearly_investment,
        "security_fee": security_fee,
        "bank_fee": bank_fee,
        "capgains_tax": capgains_tax,
        "years": years,
    }
    return contract
