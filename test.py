from foliotrack import Security
from foliotrack import Equilibrate
from foliotrack import Portfolio
from foliotrack import Currency

security1 = Security(
    name="Amundi MSCI World UCITS Security",
    ticker="AMDW",
    currency="EUR",
    price_in_security_currency=500.0,
    yearly_charge=0.2,
    target_share=0.5,
    number_held=20.0,
)
