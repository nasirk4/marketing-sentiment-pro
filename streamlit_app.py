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
    # Show fixed top navigation links
    show_top_navigation()
    
    # Show API status in sidebar
    show_api_status()
    
    # Render the main UI (includes the complete sidebar)
    render_ui()

def show_top_navigation():
    """Show fixed navigation links at the top right corner."""
    st.markdown("""
    <style>
    .fixed-nav {
        position: fixed;
        top: 15px;
        right: 20px;
        z-index: 9999;
        background: rgba(255, 255, 255, 0.95);
        padding: 10px 15px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border: 1px solid #e0e0e0;
        backdrop-filter: blur(5px);
        font-family: 'Source Sans Pro', sans-serif;
    }
    .fixed-nav a {
        margin: 0 10px;
        text-decoration: none;
        color: #1f77b4;
        font-weight: 600;
        font-size: 14px;
        transition: color 0.2s ease;
    }
    .fixed-nav a:hover {
        color: #ff4b4b;
        text-decoration: none;
    }
    .nav-spacer {
        height: 60px;
    }
    </style>
    
    <div class="fixed-nav">
        <a href="https://github.com/nasirk4/marketing-sentiment-pro" target="_blank" title="Documentation">📖 Docs</a>
        <a href="https://github.com/nasirk4/marketing-sentiment-pro/issues" target="_blank" title="Report Issues">🐛 Issues</a>
        <a href="https://github.com/nasirk4/marketing-sentiment-pro" target="_blank" title="Star on GitHub">⭐ Star</a>
    </div>
    
    <div class="nav-spacer"></div>
    """, unsafe_allow_html=True)

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

if __name__ == "__main__":
    main()