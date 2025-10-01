import numpy as np
import matplotlib.pyplot as plt


def simulate_contract(
    initial, annual_return, years, security_fee, bank_fee, yearly_contribution=0.0
):
    """
    Simulate yearly portfolio value after applying gross return, Security fee and bank fee.
    Fees (security_fee, bank_fee) are annual percentages (e.g. 0.005 for 0.5%).
    Returns (values_by_year, total_invested).
    values_by_year: numpy array of length (years+1) including year 0 (initial).
    """
    values = np.empty(years + 1)
    values[0] = initial
    invested = initial
    for y in range(1, years + 1):
        # apply gross return
        val = values[y - 1] * (1.0 + annual_return)
        # apply Security expense ratio (reduces return)
        val *= 1.0 - security_fee
        # apply bank annual fee (as % of assets at year end)
        val *= 1.0 - bank_fee
        # add yearly contribution at year end (after fees)
        if yearly_contribution:
            val += yearly_contribution
            invested += yearly_contribution
        values[y] = val
    return values, invested


def compute_after_tax_curve(values, invested, capital_gains_tax):
    """
    Compute after-tax portfolio value at each year, as if liquidated at that year.
    Returns a numpy array of after-tax values (same length as values).
    """
    gains = np.maximum(0.0, values - invested)
    taxes = gains * capital_gains_tax
    after_tax = values - taxes
    return after_tax


def parse_contract_arg(contract_str):
    """
    Parse a contract string of the form:
    "label,security_fee,bank_fee,capgains_tax"
    Example: "A,0.0059,0.006,0.172"
    Returns: dict with keys label, security_fee, bank_fee, capgains_tax
    """
    parts = contract_str.split(",")
    if len(parts) != 4:
        raise ValueError("Contract must be: label,security_fee,bank_fee,capgains_tax")
    label = parts[0].strip()
    security_fee = float(parts[1])
    bank_fee = float(parts[2])
    capgains_tax = float(parts[3])
    return {
        "label": label,
        "security_fee": security_fee,
        "bank_fee": bank_fee,
        "capgains_tax": capgains_tax,
    }
