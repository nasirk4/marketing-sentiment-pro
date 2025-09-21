# 🐦 Twitter API wrapper
import tweepy
import streamlit as st
from app.config import *

def get_api_client():
    """Authenticates and returns a Twitter API client."""
    try:
        auth = tweepy.OAuthHandler(st.secrets[CONSUMER_KEY_SECRET_NAME], st.secrets[CONSUMER_SECRET_SECRET_NAME])
        auth.set_access_token(st.secrets[ACCESS_TOKEN_SECRET_NAME], st.secrets[ACCESS_TOKEN_SECRET_SECRET_NAME])
        return tweepy.API(auth)
    except KeyError as e:
        raise Exception(f"Twitter API key not found in secrets: {e}. Please check your Streamlit secrets configuration.")
    except Exception as e:
        raise Exception(f"Failed to authenticate with Twitter API: {e}")

def fetch_tweets(api_client, mode, query, count, include_retweets):
    """Fetches tweets based on mode (keyword or user)."""
    try:
        if mode == "Keyword/Hashtag":
            search_query = f"{query} -filter:retweets" if not include_retweets else query
            tweets = tweepy.Cursor(api_client.search_tweets, q=search_query, lang="en", tweet_mode='extended').items(count)
        else:  # User Timeline
            tweets = tweepy.Cursor(api_client.user_timeline, screen_name=query, count=count, tweet_mode='extended', include_rts=include_retweets).items(count)
        return [tweet.full_text for tweet in tweets]
    except tweepy.TooManyRequests:
        raise Exception("Twitter API rate limit exceeded. Please wait a few minutes before trying again.")
    except tweepy.NotFound:
        raise Exception(f"Twitter user '@{query}' not found.")
    except Exception as e:
        raise Exception(f"An error occurred while fetching tweets: {e}")