# 🐦 Twitter API wrapper (Dual API version support)
import tweepy
import streamlit as st
from app.config import *

def get_api_client():
    """Authenticates and returns Twitter API clients for both v1.1 and v2."""
    try:
        # API v1.1 client (for user_timeline if available)
        auth_v1 = tweepy.OAuthHandler(
            st.secrets[CONSUMER_KEY_SECRET_NAME], 
            st.secrets[CONSUMER_SECRET_SECRET_NAME]
        )
        auth_v1.set_access_token(
            st.secrets[ACCESS_TOKEN_SECRET_NAME], 
            st.secrets[ACCESS_TOKEN_SECRET_SECRET_NAME]
        )
        api_v1 = tweepy.API(auth_v1)
        
        # API v2 client (preferred for search)
        client_v2 = tweepy.Client(
            bearer_token=st.secrets[BEARER_TOKEN_SECRET_NAME],
            consumer_key=st.secrets[CONSUMER_KEY_SECRET_NAME],
            consumer_secret=st.secrets[CONSUMER_SECRET_SECRET_NAME],
            access_token=st.secrets[ACCESS_TOKEN_SECRET_NAME],
            access_token_secret=st.secrets[ACCESS_TOKEN_SECRET_SECRET_NAME],
            wait_on_rate_limit=True
        )
        
        return api_v1, client_v2
        
    except KeyError as e:
        raise Exception(f"Twitter API key not found in secrets: {e}. Please check your Streamlit secrets configuration.")
    except Exception as e:
        raise Exception(f"Failed to authenticate with Twitter API: {e}")

def fetch_tweets(api_v1, client_v2, mode, query, count, include_retweets):
    """Fetches tweets using API v2 first, falls back to v1.1, then to demo data."""
    
    # Try Twitter API v2 first (most modern)
    try:
        if mode == "Keyword/Hashtag":
            # Build search query for v2
            search_query = f"{query} -is:retweet" if not include_retweets else query
            search_query += " lang:en"
            
            # Use v2 search endpoint
            response = client_v2.search_recent_tweets(
                query=search_query,
                max_results=min(count, 100),  # v2 max per request
                tweet_fields=['author_id', 'created_at', 'text']
            )
            
            if response and response.data:
                st.success("✅ Using Twitter API v2 (search_recent_tweets)")
                return [tweet.text for tweet in response.data]
                
        else:  # User Timeline
            # Get user ID first
            user_response = client_v2.get_user(username=query)
            if user_response and user_response.data:
                user_id = user_response.data.id
                
                # Get user tweets
                response = client_v2.get_users_tweets(
                    id=user_id,
                    max_results=min(count, 100),
                    exclude=['retweets'] if not include_retweets else None,
                    tweet_fields=['created_at', 'text']
                )
                
                if response and response.data:
                    st.success("✅ Using Twitter API v2 (get_users_tweets)")
                    return [tweet.text for tweet in response.data]
                    
    except tweepy.TweepyException as e:
        print(f"Twitter API v2 failed: {e}")
        # Continue to try v1.1
    
    # Fallback to Twitter API v1.1
    try:
        if mode == "Keyword/Hashtag":
            search_query = f"{query} -filter:retweets" if not include_retweets else query
            tweets = tweepy.Cursor(api_v1.search_tweets, q=search_query, lang="en", tweet_mode='extended').items(count)
            tweet_list = [tweet.full_text for tweet in tweets]
            if tweet_list:
                st.info("ℹ️ Using Twitter API v1.1 (search_tweets)")
                return tweet_list
        else:  # User Timeline
            tweets = tweepy.Cursor(api_v1.user_timeline, screen_name=query, count=count, tweet_mode='extended', include_rts=include_retweets).items(count)
            tweet_list = [tweet.full_text for tweet in tweets]
            if tweet_list:
                st.info("ℹ️ Using Twitter API v1.1 (user_timeline)")
                return tweet_list
                
    except tweepy.TweepyException as e:
        print(f"Twitter API v1.1 also failed: {e}")
        # Continue to demo mode
    
    # Final fallback: Demo mode with sample data
    st.warning("⚠️ Using sample data for demonstration. Twitter API access may be limited.")
    
    # Generate realistic sample tweets based on the query
    sample_tweets = [
        f"Really loving the new features of {query}! This is amazing. 😊",
        f"{query} has been quite reliable for my needs. Solid performance.",
        f"Not sure how I feel about {query} lately. Some issues need fixing.",
        f"Absolutely fantastic experience with {query}! Would highly recommend.",
        f"Meh. {query} is okay I guess. Nothing special really.",
        f"Having some problems with {query} customer support. Very frustrating!",
        f"{query} completely changed how I work. Incredible tool!",
        f"Wish {query} had better documentation. Hard to figure out some features.",
        f"Just started using {query} and already seeing great results!",
        f"Disappointed with {query} recent update. Preferred the old version."
    ]
    
    # Return the requested number of sample tweets
    return sample_tweets[:min(count, len(sample_tweets))]