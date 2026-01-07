import streamlit as st
import plotly.express as px
import pandas as pd
from src.services.backtest_service import BacktestServiceWrapper


@st.fragment
def render_backtest_view(portfolio, market_service, begin_date, end_date):
    if st.button("🎬 Run backtest", key="optimize_button", width="stretch"):
        try:
            with st.spinner("Running backtest..."):
                backtest_service = BacktestServiceWrapper()
                result = backtest_service.run_backtest(
                    portfolio, market_service, begin_date, end_date
                )

            # --- 1. Equity Curve ---
            st.subheader("📈 Portfolio Evolution")
            equity_curve = result.prices
            # Rebase to 100 or keep as is? Usually result is rebased to 100 by default in simple strategies,
            # or it tracks capital. Let's plot as is.
            # Convert to meaningful dataframe for plotly
            df_equity = equity_curve.reset_index()
            df_equity.columns = ["Date", "Portfolio Value"]

            fig_equity = px.line(
                df_equity,
                x="Date",
                y="Portfolio Value",
                title="Portfolio Value Over Time",
                template="plotly_dark",
            )
            st.plotly_chart(fig_equity, use_container_width=True)

            # --- 2. Key Statistics ---
            st.subheader("📊 Key Statistics")
            # result.stats is a Series or DataFrame depending on result structure (one strategy vs multiple)
            # Assuming single strategy result, accessing the first column if it's a DataFrame
            stats = result.stats
            if isinstance(stats, pd.DataFrame):
                stats = stats.iloc[:, 0]

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Return", f"{stats.get('total_return', 0):.2%}")
            with col2:
                st.metric("CAGR", f"{stats.get('cagr', 0):.2%}")
            with col3:
                st.metric("Max Drawdown", f"{stats.get('max_drawdown', 0):.2%}")
            with col4:
                st.metric("Sharpe Ratio", f"{stats.get('daily_sharpe', 0):.2f}")

            with st.expander("See full statistics"):
                st.dataframe(stats)

            # --- 3. Monthly Returns Histogram ---
            st.subheader("📅 Monthly Returns")
            # Calculate returns from prices since return_series might not be directly available on Result object
            # result.prices is a DataFrame of equity curves
            daily_returns = result.prices.pct_change().dropna()

            # If multiple columns (multiple strategies), take the first one or average?
            # Assuming single strategy for now based on context.
            if isinstance(daily_returns, pd.DataFrame) and not daily_returns.empty:
                daily_returns = daily_returns.iloc[:, 0]

            # Resample to monthly returns
            m_returns = daily_returns.resample("M").apply(lambda x: (1 + x).prod() - 1)

            fig_hist = px.histogram(
                x=m_returns,
                nbins=30,
                title="Distribution of Monthly Returns",
                labels={"x": "Monthly Return", "y": "Count"},
                template="plotly_dark",
            )
            # Add a vertical line at 0
            fig_hist.add_vline(x=0, line_dash="dash", line_color="white")
            st.plotly_chart(fig_hist, use_container_width=True)

            # --- 4. Security Returns (Bar Chart) ---
            st.subheader("🏢 Security Returns")

            # Fetch data for individual securities to calculate their period return
            tickers = list(portfolio.securities.keys())
            if tickers:
                hist_data = market_service.get_security_historical_data(
                    tickers, start_date=begin_date
                )
                # Filter to end_date if needed (hist_data might go up to today)
                hist_data = hist_data.loc[begin_date:end_date]

                # Calculate return: (End / Start) - 1
                # Use first valid index and last valid index for each column

                # Let's do a cleaner fetch logic assuming we might need to handle the frame structure
                # Re-using the hist data we just fetched

                # Extract Close prices
                if isinstance(hist_data.columns, pd.MultiIndex):
                    close_prices = hist_data["Close"]
                else:
                    # Single ticker case
                    close_prices = (
                        hist_data["Close"]
                        if "Close" in hist_data.columns
                        else hist_data
                    )

                # Calculate returns
                # We need to make sure we have data
                if not close_prices.empty:
                    # Percentage change from start to end
                    # We accept that start might be slightly different per asset if data is missing,
                    # but ffill was done in service.

                    if isinstance(close_prices, pd.DataFrame):
                        period_returns = (
                            close_prices.iloc[-1] / close_prices.iloc[0]
                        ) - 1
                        df_sec_returns = pd.DataFrame(
                            {
                                "Security": period_returns.index,
                                "Return": period_returns.values,
                            }
                        )
                    else:
                        # Single series
                        ret = (close_prices.iloc[-1] / close_prices.iloc[0]) - 1
                        df_sec_returns = pd.DataFrame(
                            {"Security": [tickers[0]], "Return": [ret]}
                        )

                    # Plot
                    fig_bar = px.bar(
                        df_sec_returns,
                        x="Security",
                        y="Return",
                        title="Period Return by Security",
                        color="Return",
                        color_continuous_scale=px.colors.diverging.RdYlGn,
                        template="plotly_dark",
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.warning("No price data found for securities.")

        except Exception as e:
            st.error(f"Backtest computation failed: {e}")
            # Raise for debugging if needed, but st.error is good for UI
            # raise e
