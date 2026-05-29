import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

prices = pd.read_csv("close_prices.csv", index_col=0, parse_dates=True)
daily_returns = prices.pct_change()
aapl = prices["AAPL"]

# Create a 3x2 grid = 6 charts in ONE long window
fig, axes = plt.subplots(3, 2, figsize=(16, 16))
fig.suptitle("Financial Analytics Dashboard", fontsize=16)

# Chart 1: Prices over time
prices.plot(ax=axes[0, 0], title="Stock Prices")

# Chart 2: Normalized comparison
(prices / prices.iloc[0] * 100).plot(ax=axes[0, 1], title="Performance (Base 100)")

# Chart 3: Correlation heatmap
sns.heatmap(daily_returns.corr(), annot=True, cmap="coolwarm", ax=axes[1, 0])
axes[1, 0].set_title("Correlation")

# Chart 4: AAPL moving averages
axes[1, 1].plot(aapl, label="Price")
axes[1, 1].plot(aapl.rolling(20).mean(), label="20-Day MA")
axes[1, 1].plot(aapl.rolling(50).mean(), label="50-Day MA")
axes[1, 1].set_title("AAPL Moving Averages")
axes[1, 1].legend()

# Chart 5: AAPL RSI
delta = aapl.diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)
rs = gain.rolling(14).mean() / loss.rolling(14).mean()
rsi = 100 - (100 / (1 + rs))
axes[2, 0].plot(rsi, color="purple", label="RSI")
axes[2, 0].axhline(70, color="red", linestyle="--")
axes[2, 0].axhline(30, color="green", linestyle="--")
axes[2, 0].set_title("AAPL RSI")
axes[2, 0].legend()

# Chart 6: Daily returns of AAPL
axes[2, 1].plot(daily_returns["AAPL"], color="gray")
axes[2, 1].set_title("AAPL Daily Returns")

# Rotate date labels and add spacing so nothing overlaps
for ax in axes.flat:
    ax.tick_params(axis="x", labelrotation=45, labelsize=8)
    ax.tick_params(axis="y", labelsize=8)

plt.tight_layout(pad=3.0)
plt.subplots_adjust(hspace=0.5, wspace=0.3)
plt.show()