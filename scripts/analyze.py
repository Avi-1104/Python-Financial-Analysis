import pandas as pd

# Load the data we saved earlier
prices = pd.read_csv("close_prices.csv", index_col=0, parse_dates=True)

# Show the first 5 rows
print(prices.head())

# Calculate daily returns (% change from one day to the next)
daily_returns = prices.pct_change()

# Show the first 5 rows of returns
print("\nDaily Returns:")
print(daily_returns.head())

# Total return over the whole period (last price vs first price)
total_return = (prices.iloc[-1] / prices.iloc[0] - 1) * 100

print("\nTotal Return over the period (%):")
print(total_return.round(2))

# Volatility = how much the daily returns jump around (risk)
# We annualize it (scale daily to yearly) by multiplying by the square root of 252 trading days
volatility = daily_returns.std() * (252 ** 0.5) * 100

print("\nVolatility / Risk (%):")
print(volatility.round(2))

# Sharpe Ratio = return per unit of risk (higher is better)
# Average daily return, annualized, divided by volatility
avg_annual_return = daily_returns.mean() * 252 * 100
sharpe_ratio = avg_annual_return / volatility

print("\nSharpe Ratio (higher = better risk-adjusted return):")
print(sharpe_ratio.round(2))

# Combine all our metrics into one clean summary table
summary = pd.DataFrame({
    "Total Return (%)": total_return.round(2),
    "Volatility (%)": volatility.round(2),
    "Sharpe Ratio": sharpe_ratio.round(2)
})

print("\n========== ANALYST SUMMARY ==========")
print(summary)
print("=====================================")

# Automatically pick out the highlights
print("\nBest Performer:", total_return.idxmax())
print("Most Volatile:", volatility.idxmax())
print("Best Risk-Adjusted (Sharpe):", sharpe_ratio.idxmax())