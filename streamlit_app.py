# 🚀 Main entry point for Streamlit
import streamlit as st
from app.ui import render_ui
from app.config import (
    CONSUMER_KEY_SECRET_NAME,
    CONSUMER_SECRET_SECRET_NAME,
    ACCESS_TOKEN_SECRET_NAME,
    ACCESS_TOKEN_SECRET_SECRET_NAME,
    BEARER_TOKEN_SECRET_NAME
)

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

    # Define required secret keys using centralized config
    REQUIRED_KEYS = [
        CONSUMER_KEY_SECRET_NAME,
        CONSUMER_SECRET_SECRET_NAME,
        ACCESS_TOKEN_SECRET_NAME,
        ACCESS_TOKEN_SECRET_SECRET_NAME,
        BEARER_TOKEN_SECRET_NAME
    ]

    # Optional: Debug output for development
    if st.secrets.get("DEBUG_MODE") == "true":
        st.write("🔍 DEBUG: Required keys to check:", REQUIRED_KEYS)
        st.write("🔍 DEBUG: Available secrets keys:", list(st.secrets.keys()))
        st.write("🔍 DEBUG: Config values:")
        st.write(f"CONSUMER_KEY_SECRET_NAME = {CONSUMER_KEY_SECRET_NAME}")
        st.write(f"CONSUMER_SECRET_SECRET_NAME = {CONSUMER_SECRET_SECRET_NAME}")
        st.write(f"ACCESS_TOKEN_SECRET_NAME = {ACCESS_TOKEN_SECRET_NAME}")
        st.write(f"ACCESS_TOKEN_SECRET_SECRET_NAME = {ACCESS_TOKEN_SECRET_SECRET_NAME}")
        st.write(f"BEARER_TOKEN_SECRET_NAME = {BEARER_TOKEN_SECRET_NAME}")

    # Validate secrets before proceeding
    validate_secrets(REQUIRED_KEYS)

    # Launch the UI
    render_ui()

if __name__ == "__main__":
    main()