from foliotrack.services.OptimizationService import (
    OptimizationService as FoliotrackOptimizationService,
)
from foliotrack.domain.Portfolio import Portfolio


class OptimizationService:
    def __init__(self):
        self.optimizer = FoliotrackOptimizationService()

    def solve_equilibrium(
        self,
        portfolio: Portfolio,
        investment_amount: float,
        min_percent_to_invest: float,
        max_different_securities: int,
        selling: bool,
    ):
        return self.optimizer.solve_equilibrium(
            portfolio,
            investment_amount=investment_amount,
            min_percent_to_invest=min_percent_to_invest,
            max_different_securities=max_different_securities,
            selling=selling,
        )
