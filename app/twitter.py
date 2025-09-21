# 🐦 Twitter API wrapper with intelligent rate limiting and demo capabilities
import streamlit as st
import time
import random
from datetime import datetime, timedelta
import json

# Global state for rate limiting
class TwitterAPIState:
    def __init__(self):
        self.last_api_call = 0
        self.call_count = 0
        self.rate_limited_until = 0
        self.demo_mode = True  # Start in demo mode by default
        
    def can_make_api_call(self):
        current_time = time.time()
        # Check if we're rate limited
        if current_time < self.rate_limited_until:
            return False
        # Enforce minimum 2 seconds between calls
        if current_time - self.last_api_call < 2:
            time.sleep(2 - (current_time - self.last_api_call))
        return True
    
    def record_api_call(self):
        self.last_api_call = time.time()
        self.call_count += 1
    
    def set_rate_limited(self, wait_time=900):
        self.rate_limited_until = time.time() + wait_time

# Global state instance
api_state = TwitterAPIState()

def get_api_client():
    """Safely get API clients with rate limit protection."""
    if not api_state.can_make_api_call():
        return None, None
    
    try:
        # Check if we have valid credentials
        if not has_valid_api_credentials():
            return None, None
            
        import tweepy
        
        # API v1.1 client
        auth_v1 = tweepy.OAuth1UserHandler(
            st.secrets.get("TWITTER_API_KEY", "demo"), 
            st.secrets.get("TWITTER_API_SECRET", "demo"),
            st.secrets.get("TWITTER_ACCESS_TOKEN", "demo"), 
            st.secrets.get("TWITTER_ACCESS_TOKEN_SECRET", "demo")
        )
        api_v1 = tweepy.API(auth_v1, wait_on_rate_limit=False)
        
        # API v2 client
        client_v2 = tweepy.Client(
            bearer_token=st.secrets.get("TWITTER_BEARER_TOKEN", "demo"),
            consumer_key=st.secrets.get("TWITTER_API_KEY", "demo"),
            consumer_secret=st.secrets.get("TWITTER_API_SECRET", "demo"),
            access_token=st.secrets.get("TWITTER_ACCESS_TOKEN", "demo"),
            access_token_secret=st.secrets.get("TWITTER_ACCESS_TOKEN_SECRET", "demo"),
            wait_on_rate_limit=False
        )
        
        api_state.record_api_call()
        return api_v1, client_v2
        
    except Exception as e:
        print(f"API client creation failed: {e}")
        return None, None

def has_valid_api_credentials():
    """Check if we have real API credentials (not demo placeholders)."""
    try:
        required_keys = [
            "TWITTER_API_KEY",
            "TWITTER_API_SECRET", 
            "TWITTER_ACCESS_TOKEN",
            "TWITTER_ACCESS_TOKEN_SECRET",
            "TWITTER_BEARER_TOKEN"
        ]
        
        for key in required_keys:
            value = st.secrets.get(key, "")
            if not value or value.lower() in ["demo", "placeholder", "test", "xxx"]:
                return False
        return True
    except:
        return False

def fetch_tweets_safe(mode, query, count=20, include_retweets=False):
    """
    Safely fetch tweets with intelligent fallback to demo data.
    Returns list of tweet objects with text, created_at, and source.
    """
    # Always start with demo mode for safety
    if api_state.demo_mode or not has_valid_api_credentials():
        return get_demo_tweets(query, count, recent=True)
    
    # Try to get API clients
    api_v1, client_v2 = get_api_client()
    if api_v1 is None or client_v2 is None:
        return get_demo_tweets(query, count, recent=True)
    
    try:
        # Try Twitter API v2
        tweets = try_api_v2(client_v2, mode, query, count, include_retweets)
        if tweets:
            return tweets
    except Exception as e:
        print(f"API v2 failed: {e}")
    
    # If all fails, use demo data
    return get_demo_tweets(query, count, recent=True)

def try_api_v2(client, mode, query, count, include_retweets):
    """Try to use Twitter API v2 with proper error handling."""
    try:
        if mode == "Keyword/Hashtag":
            search_query = f"{query} -is:retweet" if not include_retweets else query
            search_query += " lang:en"
            
            response = client.search_recent_tweets(
                query=search_query,
                max_results=min(count, 10),  # Very conservative limit
                tweet_fields=['text', 'created_at', 'author_id']
            )
            
            if response and response.data:
                return [{
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'source': 'twitter_api',
                    'id': f"api_{tweet.id}"
                } for tweet in response.data]
                
        else:  # User Timeline
            username = query.replace('@', '').strip()
            user_response = client.get_user(username=username)
            
            if user_response and user_response.data:
                user_id = user_response.data.id
                
                response = client.get_users_tweets(
                    id=user_id,
                    max_results=min(count, 10),  # Very conservative limit
                    exclude=['retweets'] if not include_retweets else None,
                    tweet_fields=['text', 'created_at']
                )
                
                if response and response.data:
                    return [{
                        'text': tweet.text,
                        'created_at': tweet.created_at,
                        'source': 'twitter_api',
                        'id': f"api_{tweet.id}"
                    } for tweet in response.data]
                    
    except Exception as e:
        if "rate limit" in str(e).lower() or "429" in str(e):
            api_state.set_rate_limited()
        raise e
    
    return None

def get_demo_tweets(query, count=20, recent=True):
    """Generate high-quality realistic demo tweets."""
    if query.startswith('@') or 'user' in query.lower():
        return generate_user_tweets(query, count, recent)
    else:
        return generate_keyword_tweets(query, count, recent)

def generate_keyword_tweets(query, count, recent):
    """Generate realistic tweets for keyword searches."""
    base_time = datetime.now()
    tweets = []
    
    # Different sentiment templates
    positive_templates = [
        f"Really loving {query}! This is amazing. 😊",
        f"Absolutely fantastic experience with {query}! Would highly recommend. 🚀",
        f"{query} has been great for my needs. Solid performance. 👍",
        f"Just started using {query} and already seeing great results! 🎉",
        f"{query} completely changed how I work. Incredible tool! 🤯"
    ]
    
    neutral_templates = [
        f"Currently testing {query}. So far so good. 🤔",
        f"Has anyone else tried {query}? What are your thoughts? 💭",
        f"Looking at alternatives to {query}. Any suggestions? 🔍",
        f"Reading about {query} features. Seems interesting. 📖",
        f"Attended a webinar about {query}. Good insights. 👨‍💻"
    ]
    
    negative_templates = [
        f"Not sure how I feel about {query} lately. Some issues need fixing. 😕",
        f"Having some problems with {query} customer support. Very frustrating! 😠",
        f"Wish {query} had better documentation. Hard to figure out some features. 🤨",
        f"Disappointed with {query} recent update. Preferred the old version. 👎",
        f"Struggling with {query} performance issues. Hopefully they fix it soon. ⚡"
    ]
    
    all_templates = positive_templates * 3 + neutral_templates * 2 + negative_templates * 1
    
    for i in range(min(count, 25)):
        tweet_text = random.choice(all_templates)
        
        # Create realistic timestamp
        if recent:
            time_offset = random.randint(1, 120)  # 1-120 minutes ago
        else:
            time_offset = random.randint(60, 1440)  # 1-24 hours ago
            
        created_at = base_time - timedelta(minutes=time_offset)
        
        # Determine sentiment
        if tweet_text in positive_templates:
            sentiment = "positive"
        elif tweet_text in negative_templates:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        tweets.append({
            'text': tweet_text,
            'created_at': created_at,
            'sentiment': sentiment,
            'source': 'demo_data',
            'id': f"demo_{i}_{hash(query)}"
        })
    
    return tweets

def generate_user_tweets(query, count, recent):
    """Generate realistic tweets for user timelines."""
    username = query.replace('@', '').strip()
    base_time = datetime.now()
    tweets = []
    
    user_templates = [
        f"Excited to announce our new feature release! 🚀",
        f"Looking for feedback on our latest update. What do you think? 💭",
        f"Happy to help customers solve their problems today! 😊",
        f"Dealing with some server issues. Working on a fix. ⚡",
        f"Our team is growing! Welcome to our new team members! 👋",
        f"Just reached {{followers}} followers! Thank you everyone! ❤️",
        f"Working on something big. Stay tuned for updates! 🔥",
        f"Thanks everyone for the great feedback on our product! 🙏",
        f"Having a great time at {{conference}} conference! Meet us at booth #{{number}}",
        f"Just published a new blog post about industry trends! 📚"
    ]
    
    for i in range(min(count, 20)):
        tweet_text = random.choice(user_templates)
        
        # Fill template variables
        if "{followers}" in tweet_text:
            followers = random.randint(1000, 50000)
            tweet_text = tweet_text.format(followers=f"{followers:,}")
        elif "{conference}" in tweet_text:
            conferences = ["TechCrunch", "Web Summit", "SXSW", "CES", "DevOps Days"]
            tweet_text = tweet_text.format(
                conference=random.choice(conferences),
                number=random.randint(10, 99)
            )
        
        # Add username for context
        if random.random() < 0.2:
            tweet_text = f"@{username}: {tweet_text}"
        
        # Create realistic timestamp
        if recent:
            time_offset = random.randint(1, 180)
        else:
            time_offset = random.randint(60, 2880)
            
        created_at = base_time - timedelta(minutes=time_offset)
        
        tweets.append({
            'text': tweet_text,
            'created_at': created_at,
            'source': 'demo_data',
            'username': username,
            'id': f"user_{i}_{hash(username)}"
        })
    
    return tweets

# Utility function to check API status
def get_api_status():
    """Return current API status information."""
    current_time = time.time()
    status = {
        'demo_mode': api_state.demo_mode,
        'has_credentials': has_valid_api_credentials(),
        'rate_limited': current_time < api_state.rate_limited_until,
        'rate_limit_remaining': max(0, api_state.rate_limited_until - current_time),
        'total_calls': api_state.call_count
    }
    return status