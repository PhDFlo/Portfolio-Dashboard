# Security Portfolio Optimizer

## Overview

The Security Portfolio Optimizer is a web application built with Streamlit that allows users to manage and optimize their security portfolios. The application provides tools for loading and updating portfolios, calculating equilibrium, buying securities, and exporting portfolio data.

## Features

- **Portfolio Management**: Load and update your security portfolios.
- **Equilibrium Calculation**: Calculate the equilibrium of your portfolio.
- **Buy Securities**: Buy new securities to add to your portfolio.
- **Compare Securities**: Compare different security contracts based on fees and capital gains tax.
- **Export Data**: Export your portfolio data for further analysis.

## Installation

To run the Security Portfolio Optimizer, you need to have Python 3.12 or later installed. Follow these steps to set up the project:

1. Clone the repository:

   ```bash
   git clone https://github.com/PhDFlo/Portfolio-Dashboard.git
   cd Portfolio-Dashboard
   ```

2. Create a virtual environment with [uv](https://github.com/astral-sh/uv) and activate it:

   ```bash
   uv venv
   source .venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   uv sync
   ```

## Usage

To start the application, run the following command:

```bash
streamlit run dashboard.py
```

This will launch the web application in your default browser. You can then use the application to manage and optimize your security portfolios.

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
