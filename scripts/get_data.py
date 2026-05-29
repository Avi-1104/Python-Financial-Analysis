import yfinance as yf

# Download data for several companies at once
stocks = yf.download(["AAPL", "MSFT", "GOOGL"], period="6mo")

# Keep only the closing prices
close_prices = stocks["Close"]

# Save the data cleanly (one clear header row)
close_prices.to_csv("close_prices.csv")
print("Saved cleanly!")