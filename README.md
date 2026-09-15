# Historical and Monte Carlo Value-at-Risk Engine for Dow Jones Portfolios

Market-risk engine using 10 years of daily adjusted prices for 30 Dow Jones stocks, SQLite, historical VaR, vectorized Monte Carlo VaR and Kupiec backtesting.

## Run
`pip install -r requirements.txt`
`python scripts/download_data.py --years 10`
`python scripts/run_var.py --paths 100000 --confidence 0.99`
`python scripts/backtest.py --days 1250 --confidence 0.99`
`pytest -q`

The market data is fetched at runtime with yfinance and is not bundled. Exact row counts and backtest breaches can vary as Yahoo Finance data changes.

## Data validation
`app/validation.py` checks duplicate ticker/date rows, non-positive prices, missing business dates and unusually large daily moves. Adjusted close is used so ordinary split/dividend effects are represented in the adjusted series.

## Historical VaR
At 99% confidence:
`VaR = -quantile(portfolio_daily_returns, 0.01)`

## Monte Carlo VaR
Historical mean/covariance are used to generate correlated normal returns. Cholesky decomposition creates the correlation structure, while NumPy matrix operations generate all paths without Python loops.

The project description's benchmark is 100,000 paths in about 1.6 seconds versus 41 seconds for a loop implementation. Run `python scripts/benchmark.py --paths 100000` to measure the actual machine.

## Backtest
A rolling historical 99% one-day VaR is compared with the next realized portfolio return over 1,250 trading days. A breach occurs when realized return is below `-VaR`. Kupiec's unconditional coverage statistic tests whether the observed breach rate is consistent with the expected 1% rate.

The description mentions 18 breaches; the code calculates the actual number from downloaded data rather than hard-coding it.

## Interview file flow
`scripts/download_data.py` -> `app/validation.py` -> `app/database.py` -> `app/var_engine.py` -> `scripts/run_var.py`; `scripts/backtest.py` performs rolling validation and Kupiec's test.
