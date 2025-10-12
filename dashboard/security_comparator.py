import numpy as np


def simulate_contract(
    initial, annual_return, years, security_fee, bank_fee, yearly_contribution=0.0
):
    """
    Simulate yearly portfolio value after applying gross return, Security fee and bank fee.

    Parameters:
        initial (float): initial investment
        annual_return (float): annual gross return
        years (int): number of years to simulate
        security_fee (float): annual security expense ratio (e.g. 0.005 for 0.5%)
        bank_fee (float): annual bank fee (as percentage of assets at year end)
        yearly_contribution (float, optional): yearly investment amount (default is 0)

    Returns:
        tuple: (values_by_year, total_invested)
            values_by_year (numpy array): portfolio values at each year
            total_invested (float): total amount invested
    """
    # Initialize array to store values at each year
    values = np.empty(years + 1)
    values[0] = initial
    # Initialize total invested
    invested = initial
    # Simulate yearly portfolio value
    for y in range(1, years + 1):
        # Apply gross return
        val = values[y - 1] * (1.0 + annual_return)
        # Apply security expense ratio (reduces return)
        val *= 1.0 - security_fee
        # Apply bank annual fee (as % of assets at year end)
        val *= 1.0 - bank_fee
        # Add yearly contribution at year end (after fees)
        if yearly_contribution:
            val += yearly_contribution
            invested += yearly_contribution
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
    default_label="Contract",
    default_initial=10000.0,
    default_annual_return=0.06,
    default_yearly_investment=0.0,
    default_security_fee=0.005,
    default_bank_fee=0.005,
    default_capgains_tax=0.3,
):
    """
    Create a contract form in the Streamlit app with default values and labels.

    Parameters:
        st (Streamlit): the Streamlit app object
        key_prefix (str): prefix for the form field keys
        default_label (str): default label for the contract
        default_initial (float): default initial investment
        default_annual_return (float): default annual return
        default_yearly_investment (float): default yearly investment
        default_security_fee (float): default security fee
        default_bank_fee (float): default bank fee
        default_capgains_tax (float): default capital gains tax

    Returns:
        contract (dict): a dictionary containing the contract form values
    """
    st.subheader(f"Contract {key_prefix.upper()}")
    label = st.text_input(
        "Label",
        value=f"{default_label}",
        key=f"label_{key_prefix}",
    )
    initial = st.number_input(
        f"Initial Investment (e.g. {default_initial}€)",
        value=default_initial,
        format="%.2f",
        key=f"initial_{key_prefix}",
    )
    annual_return = st.number_input(
        f"Annual Return (e.g. {default_annual_return} for {default_annual_return * 100}%)",
        value=default_annual_return,
        format="%.3f",
        min_value=0.0,
        max_value=1.0,
        key=f"annual_return_{key_prefix}",
    )
    yearly_investment = st.number_input(
        f"Yearly Investment (e.g. {default_yearly_investment}€) ",
        value=default_yearly_investment,
        format="%.2f",
        key=f"yearly_investment_{key_prefix}",
    )
    security_fee = st.number_input(
        f"Annual Security Fee (e.g. {default_security_fee} for {default_security_fee * 100}%)",
        value=default_security_fee,
        format="%.3f",
        min_value=0.0,
        max_value=1.0,
        key=f"security_fee_{key_prefix}",
    )
    bank_fee = st.number_input(
        f"Annual Bank Fee (e.g. {default_bank_fee} for {default_bank_fee * 100}%)",
        value=default_bank_fee,
        format="%.3f",
        min_value=0.0,
        max_value=1.0,
        key=f"bank_fee_{key_prefix}",
    )
    capgains_tax = st.number_input(
        f"Capital Gains Tax (e.g. {default_capgains_tax} for {default_capgains_tax * 100}%)",
        value=default_capgains_tax,
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
    }
    return contract
