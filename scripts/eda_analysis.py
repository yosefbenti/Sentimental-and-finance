import sys
print("Python executable:", sys.executable)

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from collections import Counter

# Ensure NLTK stopwords are downloaded
nltk.download('stopwords')

# Load dataset
df = pd.read_csv("./data/raw_analyst_ratings.csv")  # Update path if needed

# Descriptive Statistics
df['headline_len'] = df['headline'].astype(str).apply(len)
print("Headline Length Statistics:")
print(df['headline_len'].describe())

# Articles per Publisher
publisher_counts = df['publisher'].value_counts()
print("\nArticles per Publisher:")
print(publisher_counts)

# Publication Date Trends
# Fix date parsing with infer_datetime_format or explicit format
df['date'] = pd.to_datetime(df['date'], errors='coerce', infer_datetime_format=True)

# Group articles by day
articles_per_day = df.groupby(df['date'].dt.date).size()

# Plot number of articles per day
plt.figure(figsize=(12, 6))
articles_per_day.plot()
plt.title('Number of Articles per Day')
plt.xlabel('Date')
plt.ylabel('Number of Articles')
plt.tight_layout()
plt.show()

# Word Cloud for Headlines
stop_words = set(stopwords.words('english'))
headlines = df['headline'].dropna().astype(str).tolist()
words = ' '.join(headlines).lower().split()
filtered_words = [word for word in words if word.isalpha() and word not in stop_words]

word_counts = Counter(filtered_words)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)

plt.figure(figsize=(15, 7.5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Headlines')
plt.show()
