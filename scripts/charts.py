import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data we saved earlier
prices = pd.read_csv("close_prices.csv", index_col=0, parse_dates=True)

# Draw a line chart of all stocks
prices.plot(figsize=(10, 5), title="Stock Prices Over Time")

plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.grid(True)
plt.show()

# Normalize: make every stock start at 100 for a fair comparison
normalized = prices / prices.iloc[0] * 100

normalized.plot(figsize=(10, 5), title="Performance Comparison (Starting at 100)")

plt.xlabel("Date")
plt.ylabel("Growth (Base = 100)")
plt.grid(True)
plt.show()



# Calculate daily returns first (correlation is based on returns, not prices)
daily_returns = prices.pct_change()

# Build the correlation table
correlation = daily_returns.corr()

# Draw it as a colored heatmap
plt.figure(figsize=(7, 5))
sns.heatmap(correlation, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
plt.title("Stock Correlation Heatmap")
plt.show()

# Focus on one stock for moving averages
aapl = prices["AAPL"]

# Calculate moving averages
ma20 = aapl.rolling(window=20).mean()   # 20-day average (short-term trend)
ma50 = aapl.rolling(window=50).mean()   # 50-day average (longer-term trend)

# Plot price + both averages together
plt.figure(figsize=(10, 5))
plt.plot(aapl, label="AAPL Price")
plt.plot(ma20, label="20-Day Average")
plt.plot(ma50, label="50-Day Average")
plt.title("AAPL with Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()
plt.grid(True)
plt.show()

# --- Calculate RSI for Apple ---
delta = aapl.diff()                          # day-to-day price change
gain = delta.clip(lower=0)                   # keep only the up moves
loss = -delta.clip(upper=0)                  # keep only the down moves (as positive)

avg_gain = gain.rolling(window=14).mean()    # average gain over 14 days
avg_loss = loss.rolling(window=14).mean()    # average loss over 14 days

rs = avg_gain / avg_loss                      # relative strength
rsi = 100 - (100 / (1 + rs))                  # the RSI formula

# Plot the RSI
plt.figure(figsize=(10, 4))
plt.plot(rsi, label="RSI", color="purple")
plt.axhline(70, color="red", linestyle="--", label="Overbought (70)")
plt.axhline(30, color="green", linestyle="--", label="Oversold (30)")
plt.title("AAPL RSI (Relative Strength Index)")
plt.xlabel("Date")
plt.ylabel("RSI")
plt.legend()
plt.grid(True)
plt.show()