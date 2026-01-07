try:
    import foliotrack

    print("foliotrack found")
    print(foliotrack.__file__)

    from foliotrack.services.BacktestService import BacktestService

    print("BacktestService found")

    # Inspect BacktestService
    import inspect

    print(inspect.signature(BacktestService.run_backtest))

    # We can't easily run a backtest without data, but we can check if we can inspect the return type annotation or docstring
    print(BacktestService.run_backtest.__doc__)

except ImportError as e:
    print(f"Error: {e}")
