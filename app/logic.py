# 🧠 Core sentiment analysis logic
import pandas as pd
import streamlit as st
from datetime import datetime
from app.twitter import fetch_tweets_safe  # Updated import - removed get_api_client and include_rt
from app.utils import clean_text, get_subjectivity, get_polarity, get_sentiment_label
from app.config import MAX_TWEETS_DEMO, CACHE_TTL

@st.cache_data(ttl=CACHE_TTL, show_spinner="Fetching and analyzing social data...")
def analyze_query(mode, query, count, include_retweets):
    """
    Main pipeline: Fetches data, cleans it, and performs sentiment analysis.
    Cached to avoid hitting API limits on re-runs.
    """
    # Enforce demo limit
    count = min(count, MAX_TWEETS_DEMO)
    
    # Use the new fetch_tweets_safe function (no need for API clients)
    raw_tweets = fetch_tweets_safe(mode, query, count, include_retweets)  # Fixed parameter name
    
    if not raw_tweets:
        return pd.DataFrame()
    
    # Extract tweet texts from the new format (list of dictionaries)
    tweet_texts = [tweet['text'] for tweet in raw_tweets]
    
    # Create DataFrame and process data
    df = pd.DataFrame(tweet_texts, columns=['Raw_Tweet'])
    df['Cleaned_Tweet'] = df['Raw_Tweet'].apply(clean_text)
    # Filter out empty tweets after cleaning
    df = df[df['Cleaned_Tweet'].str.strip().astype(bool)]
    
    if df.empty:
        return df
        
    df['Subjectivity'] = df['Cleaned_Tweet'].apply(get_subjectivity)
    df['Polarity'] = df['Cleaned_Tweet'].apply(get_polarity)
    df['Sentiment'] = df['Polarity'].apply(get_sentiment_label)
    df['Analysis_Time'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    return df