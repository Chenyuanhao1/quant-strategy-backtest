# Quantitative Strategy Backtest Project
This project implements a simple moving average trading strategy and performs backtesting on simulated stock price data.

## Project Description
- Trading Rule: Buy when short moving average crosses above long moving average (golden cross); sell when death cross appears.
- Compare strategy performance with simple buy-and-hold strategy.
- Metrics calculated: total return, maximum drawdown.

## Dataset
Simulated stock price data, randomly generated, not real market data.

## Visualization
`portfolio_curve.png`: Net asset value curve comparison between strategy and buy&hold.

## How to Run
1. Install required packages: `pip install numpy pandas matplotlib`
2. Run `strategy_backtest.py`