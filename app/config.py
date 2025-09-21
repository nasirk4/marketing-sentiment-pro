# ⚙️ Constants and configuration
# Settings that might need to be changed for different deployments

# Twitter API Settings (Names mapped to Streamlit secrets)
CONSUMER_KEY_SECRET_NAME = "TWITTER_CONSUMER_KEY"
CONSUMER_SECRET_SECRET_NAME = "TWITTER_CONSUMER_SECRET"
ACCESS_TOKEN_SECRET_NAME = "TWITTER_ACCESS_TOKEN"
ACCESS_TOKEN_SECRET_SECRET_NAME = "TWITTER_ACCESS_TOKEN_SECRET"

# App Behavior Settings
MAX_TWEETS_DEMO = 200  # Safe limit for free API tier to avoid rate limits
CACHE_TTL = 600  # Time in seconds to cache data (10 minutes)