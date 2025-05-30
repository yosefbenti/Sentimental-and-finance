import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
import os

# List of companies (adjust to match your filenames)
companies = ['AAPL','AMZN', 'GOOG','META', 'MSFT','NVDA', 'TSLA']

# Load news data once
news_file = './data/raw_analyst_ratings.csv'
df_news = pd.read_csv(news_file)
df_news['date'] = pd.to_datetime(df_news['date'], errors='coerce', utc=True).dt.date

# Apply sentiment
def get_sentiment(text):
    if isinstance(text, str):
        return TextBlob(text).sentiment.polarity
    return 0

df_news['sentiment'] = df_news['headline'].apply(get_sentiment)

# Store summary results
summary_list = []

for company in companies:
    stock_file = f'./data/{company}_historical_data.csv'

    # Skip the first 4 rows and use known columns
    stock_columns = ['date', 'Price', 'Close', 'High', 'Low', 'Open', 'Volume']
    df_stock = pd.read_csv(stock_file, skiprows=4, names=stock_columns)
    df_stock['date'] = pd.to_datetime(df_stock['date'], errors='coerce').dt.date

    # Calculate daily returns
    df_stock = df_stock.sort_values('date')
    df_stock['daily_return'] = df_stock['Close'].pct_change()
    df_returns = df_stock[['date', 'daily_return']].dropna()

    # Filter news for this company only
    df_news_filtered = df_news[df_news['headline'].str.contains(company, na=False)]
    daily_sentiment = df_news_filtered.groupby('date')['sentiment'].mean().reset_index()

    # Merge
    merged_df = pd.merge(daily_sentiment, df_returns, on='date')

    # Summary stats
    correlation = merged_df['sentiment'].corr(merged_df['daily_return'], method='pearson')
    sentiment_mean = daily_sentiment['sentiment'].mean()
    return_mean = df_returns['daily_return'].mean()
    count = len(df_news_filtered)

    summary_list.append({
        'Company': company,
        'Avg Sentiment': round(sentiment_mean, 4),
        'Headline Count': count,
        'Avg Return': round(return_mean, 4),
        'Pearson Corr': round(correlation, 4) if not pd.isna(correlation) else 'N/A'
    })

# Create summary table
summary_df = pd.DataFrame(summary_list)
print(summary_df)

# Save visual
sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))
sns.barplot(data=summary_df, x='Company', y='Avg Sentiment', palette='viridis')
plt.title('Average Sentiment by Company')
plt.tight_layout()
os.makedirs('outputs', exist_ok=True)
plt.savefig('outputs/avg_sentiment_by_company.png')
plt.show()
