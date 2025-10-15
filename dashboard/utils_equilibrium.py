import pandas as pd


def eqportfolio2df(portfolio):
    """Convert portfolio info to DataFrame format for display"""
    info = portfolio.get_portfolio_info()
    data = []
    for security in info:
        data.append(
            {
                "Name": security.get("name"),
                "Ticker": security.get("ticker"),
                "Currency": security.get("currency"),
                "Price": security.get("price_in_security_currency"),
                "Target Share": security.get("target_share"),
                "Actual Share": security.get("actual_share"),
                "Final Share": security.get("final_share"),
                "Amount to Invest": security.get("amount_to_invest"),
                "Number to buy": security.get("number_to_buy"),
            }
        )
    return pd.DataFrame(data)
