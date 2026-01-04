from foliotrack.services.BacktestService import (
    BacktestService as FoliotrackBacktestService,
)
from foliotrack.domain.Portfolio import Portfolio


class BacktestServiceWrapper:
    def __init__(self):
        self.service = FoliotrackBacktestService()

    def run_backtest(self, portfolio: Portfolio, market_service, start_date, end_date):
        return self.service.run_backtest(
            portfolio,
            market_service,
            start_date=start_date,
            end_date=end_date,
        )
