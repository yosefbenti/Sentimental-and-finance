import yfinance as yf
import talib

# Download data
data = yf.download("AAPL", start="2022-01-01", end="2023-01-01")
data.dropna(inplace=True)

# Ensure close_prices is 1D numpy array
close_prices = data['Close'].to_numpy().flatten()

# Calculate 20-day SMA
data['SMA_20'] = talib.SMA(close_prices, timeperiod=20)

print(data[['Close', 'SMA_20']].tail())
