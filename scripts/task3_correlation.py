import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
import os

# File paths
stock_file = './data/AAPL_stock_data.csv'
news_file = './data/raw_analyst_ratings.csv'

# Define correct column names manually
stock_columns = ['date', 'Price', 'Close', 'High', 'Low', 'Open', 'Volume']

# Load stock data skipping first 4 rows and add header manually
df_stock = pd.read_csv(stock_file, skiprows=4, names=stock_columns)

print("Stock data columns after loading:", df_stock.columns.tolist())
print("First few rows:\n", df_stock.head())

# Convert date column to datetime.date (stock)
df_stock['date'] = pd.to_datetime(df_stock['date'], errors='coerce').dt.date

# Load news data
df_news = pd.read_csv(news_file)

print("News data columns after loading:", df_news.columns.tolist())
print("First few rows:\n", df_news.head())

# Parse news dates with UTC and convert to date only
df_news['date'] = pd.to_datetime(df_news['date'], errors='coerce', utc=True).dt.date

# Check for any unparsable dates in news
if df_news['date'].isna().any():
    print("Warning: Some news dates could not be parsed:")
    print(df_news[df_news['date'].isna()])

# Sentiment analysis on headlines using TextBlob
def get_sentiment(text):
    if isinstance(text, str):
        return TextBlob(text).sentiment.polarity
    return 0

df_news['sentiment'] = df_news['headline'].apply(get_sentiment)

# Aggregate daily sentiment
daily_sentiment = df_news.groupby('date')['sentiment'].mean().reset_index()

# Compute daily stock returns based on 'Close' price
df_stock = df_stock.sort_values('date')
df_stock['daily_return'] = df_stock['Close'].pct_change()
df_returns = df_stock[['date', 'daily_return']].dropna()

# Merge sentiment and returns on date
merged_df = pd.merge(daily_sentiment, df_returns, on='date')

# Calculate Pearson correlation
correlation = merged_df['sentiment'].corr(merged_df['daily_return'], method='pearson')
print(f"📊 Pearson Correlation between Sentiment and Stock Return: {correlation:.4f}")

# Optional: Visualize the relationship
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=merged_df, x='sentiment', y='daily_return', color='royalblue')
plt.title('Sentiment vs Stock Return')
plt.xlabel('Average Daily Sentiment')
plt.ylabel('Daily Stock Return')
plt.tight_layout()

# Ensure output directory exists
os.makedirs('outputs', exist_ok=True)
plt.savefig('outputs/sentiment_stock_correlation.png')
plt.show()
