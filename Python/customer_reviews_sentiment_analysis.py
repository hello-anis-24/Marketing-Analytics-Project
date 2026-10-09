

import pandas as pd
import pyodbc
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


# ---------------------------------------------------------
# 1. Download the VADER lexicon
# ---------------------------------------------------------

# VADER uses this lexicon to analyze sentiment in text.
nltk.download('vader_lexicon')


# ---------------------------------------------------------
# 2. Fetch customer review data from SQL Server
# ---------------------------------------------------------

def fetch_data_from_sql():

    # Connection details for SQL Server
    conn_str = (
        "Driver={SQL Server};"
        "Server=DESKTOP-R6ID14N\\SQLEXPRESS;"
        "Database=MarketingAnalytics;"
        "Trusted_Connection=yes;"
    )

    # Establish connection to SQL Server
    conn = pyodbc.connect(conn_str)

    # SQL query to retrieve customer review data
    query = """
        SELECT
            ReviewID,
            CustomerID,
            ProductID,
            ReviewDate,
            Rating,
            ReviewText
        FROM dbo.customer_reviews
    """

    # Load SQL data into a Pandas DataFrame
    df = pd.read_sql(query, conn)

    # Close the database connection
    conn.close()

    # Return the DataFrame
    return df


# Fetch customer review data
customer_reviews_df = fetch_data_from_sql()


# ---------------------------------------------------------
# 3. Initialize VADER Sentiment Analyzer
# ---------------------------------------------------------

sia = SentimentIntensityAnalyzer()


# ---------------------------------------------------------
# 4. Calculate Sentiment Score
# ---------------------------------------------------------

def calculate_sentiment(review):

    # Handle missing review text
    if pd.isna(review):
        return 0.0

    # Analyze the review text using VADER
    sentiment = sia.polarity_scores(str(review))

    # Return compound sentiment score
    # Range: -1 = very negative to +1 = very positive
    return sentiment['compound']


# ---------------------------------------------------------
# 5. Categorize Sentiment
# ---------------------------------------------------------

def categorize_sentiment(score, rating):

    # Positive text sentiment
    if score > 0.05:

        if rating >= 4:
            return 'Positive'

        elif rating == 3:
            return 'Mixed Positive'

        else:
            return 'Mixed Negative'

    # Negative text sentiment
    elif score < -0.05:

        if rating <= 2:
            return 'Negative'

        elif rating == 3:
            return 'Mixed Negative'

        else:
            return 'Mixed Positive'

    # Neutral text sentiment
    else:

        if rating >= 4:
            return 'Positive'

        elif rating <= 2:
            return 'Negative'

        else:
            return 'Neutral'


# ---------------------------------------------------------
# 6. Create Sentiment Score Buckets
# ---------------------------------------------------------

def sentiment_bucket(score):

    if score >= 0.5:
        return '0.5 to 1.0'

    elif 0.0 <= score < 0.5:
        return '0.0 to 0.49'

    elif -0.5 <= score < 0.0:
        return '-0.49 to 0.0'

    else:
        return '-1.0 to -0.5'


# ---------------------------------------------------------
# 7. Apply Sentiment Analysis
# ---------------------------------------------------------

# Calculate sentiment score for every customer review
customer_reviews_df['SentimentScore'] = (
    customer_reviews_df['ReviewText']
    .apply(calculate_sentiment)
)


# Create sentiment category using sentiment score and rating
customer_reviews_df['SentimentCategory'] = customer_reviews_df.apply(
    lambda row: categorize_sentiment(
        row['SentimentScore'],
        row['Rating']
    ),
    axis=1
)


# Create sentiment score bucket
customer_reviews_df['SentimentBucket'] = (
    customer_reviews_df['SentimentScore']
    .apply(sentiment_bucket)
)


# ---------------------------------------------------------
# 8. Display Results
# ---------------------------------------------------------

print(customer_reviews_df.head())


# ---------------------------------------------------------
# 9. Export Results to CSV
# ---------------------------------------------------------

customer_reviews_df.to_csv(
    'customer_reviews_with_sentiment.csv',
    index=False
)

print("\nSentiment analysis completed successfully!")
print("CSV file created: customer_reviews_with_sentiment.csv")