# Security Portfolio Optimizer

An interactive Streamlit application to load, manage and optimize a securities portfolio.

This repository contains a dashboard built around the `foliotrack` portfolio model and several Streamlit pages that let you:

- Load and save portfolio JSON files (`Portfolios/`).
- Update live prices (via the `foliotrack.Portfolio` methods).
- Compute an "equilibrium" allocation and suggest purchases to rebalance.
- Buy and sell securities from the UI.
- Compare two contract types (fees, bank fees and capital gains taxation) with interactive simulations and after-tax curves.

## Requirements

- Python >= 3.11 (see `pyproject.toml`).
- Dependencies are declared in `pyproject.toml` (including `foliotrack`, `streamlit`, `plotly`, `pytest`).

## Installation

1. Clone the repository:

```bash
git clone https://github.com/PhDFlo/Portfolio-Dashboard.git
cd Portfolio-Dashboard
```

2. Create & activate a virtual environment. Using the project's tool `uv`:

```bash
uv venv
source .venv/bin/activate
uv sync
```

## Run the app

Start the Streamlit app from the repository root:

```bash
streamlit run app.py
```

Use the left navigation to open:

- Manage → `Portfolio & Update Prices` (`pages/load_portfolio.py`)
- Manage → `Equilibrium, Buy & Export` (`pages/equilibrium_buy.py`)
- Tools → `Compare Securities` (`pages/compare_securities.py`)

## Example: load the sample portfolio

Open the `Portfolio & Update Prices` page, select `investment_example.json` from the sidebar and click `Load`.

## Tests

UI tests are provided under `tests/` and use Streamlit's `AppTest` harness. To run them locally:

```bash
uv run pytest
```

This will launch the web application in your default browser. You can then use the application to manage and optimize your security portfolios.

## License

This project is licensed under the Apache License, Version 2.0 — see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome. Please open an issue to discuss larger changes or submit pull requests for small improvements and bug fixes.
