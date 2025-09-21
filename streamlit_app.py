# 🚀 Main entry point for Streamlit
import streamlit as st
from app.ui import render_ui

# Page configuration
st.set_page_config(
    page_title="Marketing Sentiment Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'force_demo' not in st.session_state:
    st.session_state.force_demo = True

def main():
    """Main function to run the Streamlit app."""
    # Show minimalist navigation using pure Streamlit
    show_minimal_navigation()
    
    # Show API status in sidebar
    show_api_status()
    
    # Render main UI
    render_ui()

def show_minimal_navigation():
    """Minimalist text links."""
    # Create a row for navigation
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([3, 1, 1, 1])
    
    # Navigation text links
    with nav_col2:
        st.markdown("[📖 Docs](https://github.com/nasirk4/marketing-sentiment-pro)")
    
    with nav_col3:
        st.markdown("[🐛 Issues](https://github.com/nasirk4/marketing-sentiment-pro/issues)")
    
    with nav_col4:
        st.markdown("[⭐ Star](https://github.com/nasirk4/marketing-sentiment-pro)")
    
    st.divider()

def show_api_status():
    """Show API status information in sidebar."""
    # Import here to avoid circular imports
    from app.twitter import has_valid_api_credentials, get_api_status
    from app.twitter import api_state
    
    api_status = get_api_status()
    
    # Show status with clean icons
    st.sidebar.subheader("API Status")
    
    if st.session_state.force_demo:
        st.sidebar.success("✅ Demo Mode Active")
        st.sidebar.caption("Using sample data for demos")
    elif not has_valid_api_credentials():
        st.sidebar.warning("⚠️ API Not Configured")
        st.sidebar.caption("Add API keys for live data")
    elif api_status['rate_limited']:
        remaining = int(api_status['rate_limit_remaining'])
        st.sidebar.error(f"⏳ Rate Limited ({remaining}s)")
        st.sidebar.caption("Using demo data temporarily")
    else:
        st.sidebar.success("✅ Live API Active")
        st.sidebar.caption(f"API Calls: {api_status['total_calls']}")

if __name__ == "__main__":
    main()