# 🚀 Main entry point for Streamlit
from app.ui import render_ui
import streamlit as st

REQUIRED_KEYS = [
    "TWITTER_API_KEY",
    "TWITTER_API_SECRET",
    "TWITTER_ACCESS_TOKEN",
    "TWITTER_ACCESS_TOKEN_SECRET",
    "TWITTER_BEARER_TOKEN"
]

for key in REQUIRED_KEYS:
    if key not in st.secrets:
        st.error(f"Missing required secret: {key}")
        raise KeyError(f"Missing required secret: {key}")

def main():
    """Main function to run the Streamlit app."""
    render_ui()

if __name__ == "__main__":
    main()