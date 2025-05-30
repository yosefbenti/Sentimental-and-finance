import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import talib
import pynance as pn

ticker = 'AAPL'
data = yf.download(ticker, start='2022-01-01', end='2023-01-01')
data.dropna(inplace=True)

# Confirm dimension of Close prices
print(data['Close'].shape)
print(data['Close'].values.shape)
print(type(data['Close'].values))

close_prices = data['Close'].to_numpy().flatten()

data['RSI'] = talib.RSI(close_prices, timeperiod=14)
data['MACD'], data['MACD_signal'], data['MACD_hist'] = talib.MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)
data['SMA_50'] = talib.SMA(close_prices, timeperiod=50)
data['SMA_200'] = talib.SMA(close_prices, timeperiod=200)

plt.figure(figsize=(14, 7))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['SMA_50'], label='50-day SMA')
plt.plot(data['SMA_200'], label='200-day SMA')
plt.title(f'{ticker} Close Price and Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.tight_layout()
plt.show()

