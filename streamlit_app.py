# 🚀 Main entry point for Streamlit
import streamlit as st
from app.ui import render_ui

# DEBUG: Try to read the config file directly
try:
    with open('app/config.py', 'r') as f:
        config_content = f.read()
    st.write("🔍 Config file content:", config_content)
except Exception as e:
    st.error(f"❌ Cannot read config file: {e}")

# Try to import config, but provide fallbacks
try:
    from app.config import (
        CONSUMER_KEY_SECRET_NAME,
        CONSUMER_SECRET_SECRET_NAME,
        ACCESS_TOKEN_SECRET_NAME,
        ACCESS_TOKEN_SECRET_SECRET_NAME,
        BEARER_TOKEN_SECRET_NAME
    )
    st.success("✅ All config imports successful!")
except ImportError as e:
    st.error(f"❌ Config import error: {e}")
    # Fallback to hardcoded values
    CONSUMER_KEY_SECRET_NAME = "TWITTER_API_KEY"
    CONSUMER_SECRET_SECRET_NAME = "TWITTER_API_SECRET" 
    ACCESS_TOKEN_SECRET_NAME = "TWITTER_ACCESS_TOKEN"
    ACCESS_TOKEN_SECRET_SECRET_NAME = "TWITTER_ACCESS_TOKEN_SECRET"
    BEARER_TOKEN_SECRET_NAME = "TWITTER_BEARER_TOKEN"
    st.info("ℹ️ Using fallback config values")

def validate_secrets(required_keys):
    """Checks for missing secrets and raises error if any are absent."""
    missing = [key for key in required_keys if key not in st.secrets]
    if missing:
        st.error(f"❌ Missing required secrets: {', '.join(missing)}")
        st.error(f"✅ Available secrets: {list(st.secrets.keys())}")
        raise KeyError(f"Missing required secrets: {missing}")

def main():
    """Main function to run the Streamlit app."""
    # Clear any cached data/resources to avoid stale references
    st.cache_data.clear()
    st.cache_resource.clear()

    # Define required secret keys
    REQUIRED_KEYS = [
        CONSUMER_KEY_SECRET_NAME,
        CONSUMER_SECRET_SECRET_NAME,
        ACCESS_TOKEN_SECRET_NAME,
        ACCESS_TOKEN_SECRET_SECRET_NAME,
        BEARER_TOKEN_SECRET_NAME
    ]

    st.write("🔍 Required keys:", REQUIRED_KEYS)
    
    # Validate secrets before proceeding
    validate_secrets(REQUIRED_KEYS)
    render_ui()

if __name__ == "__main__":
    main()