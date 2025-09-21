# 🚀 Main entry point for Streamlit - Safe Demo Version
import streamlit as st
from app.ui import render_ui

# Page configuration
st.set_page_config(
    page_title="Marketing Sentiment Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for UI
if 'force_demo' not in st.session_state:
    st.session_state.force_demo = True  # Always start in demo mode

def main():
    """Main function to run the Streamlit app."""
    # Only show API status, render_ui() handles the main sidebar
    show_api_status()
    
    # Render the main UI (includes the complete sidebar)
    render_ui()
    
    # Add documentation links to the main app area (footer)
    show_documentation_links()

def show_api_status():
    """Show API status information in sidebar below configuration panel."""
    # Import here to avoid circular imports
    from app.twitter import has_valid_api_credentials, get_api_status
    from app.twitter import api_state
    
    api_status = get_api_status()
    
    if st.session_state.force_demo:
        st.sidebar.success("✅ Demo Mode Active")
        st.sidebar.info("Using high-quality sample data for reliable demos")
    elif not has_valid_api_credentials():
        st.sidebar.warning("⚠️ API Not Configured")
        st.sidebar.info("Add Twitter API keys to use live data")
    elif api_status['rate_limited']:
        remaining = int(api_status['rate_limit_remaining'])
        st.sidebar.error(f"⏳ Rate Limited ({remaining}s)")
    else:
        st.sidebar.success("✅ Live API Active")
        st.sidebar.info(f"API Calls: {api_status['total_calls']}")

def show_documentation_links():
    """Show documentation links in the main app area (footer)."""
    st.markdown("---")
    st.markdown(
        """
        **Links:** 
        [📖 Documentation](https://github.com/nasirk4/marketing-sentiment-pro) | 
        [🐛 Report Issues](https://github.com/nasirk4/marketing-sentiment-pro/issues) |
        [⭐ Star on GitHub](https://github.com/nasirk4/marketing-sentiment-pro)
        """
    )

if __name__ == "__main__":
    main()