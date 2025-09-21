# 🚀 Main entry point for Streamlit
import streamlit as st
from app.ui import render_ui

def validate_secrets(required_keys):
    """Checks for missing secrets and raises error if any are absent."""
    missing = [key for key in required_keys if key not in st.secrets]
    if missing:
        st.error(f"❌ Missing required secrets: {', '.join(missing)}")
        st.error(f"✅ Available secrets: {list(st.secrets.keys())}")
        raise KeyError(f"Missing required secrets: {missing}")

def main():
    """Main function to run the Streamlit app."""
    # Define required secret keys (directly from config.py values)
    REQUIRED_KEYS = [
        "TWITTER_API_KEY",
        "TWITTER_API_SECRET", 
        "TWITTER_ACCESS_TOKEN",
        "TWITTER_ACCESS_TOKEN_SECRET",
        "TWITTER_BEARER_TOKEN"
    ]

    st.write("🔍 Required keys:", REQUIRED_KEYS)
    
    # Validate secrets before proceeding
    try:
        validate_secrets(REQUIRED_KEYS)
        render_ui()
    except KeyError:
        st.error("Please add the missing secrets to your .streamlit/secrets.toml file")
        st.stop()

if __name__ == "__main__":
    main()