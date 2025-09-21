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
    # Show fixed top navigation links (HIGHEST PRIORITY)
    show_top_navigation()
    
    # Show API status in sidebar
    show_api_status()
    
    # Render the main UI (includes the complete sidebar)
    render_ui()

def show_top_navigation():
    """Show fixed navigation links at the top right corner with guaranteed visibility."""
    st.markdown("""
    <style>
    /* Highest priority navigation */
    .fixed-nav {
        position: fixed;
        top: 15px;
        right: 20px;
        z-index: 999999; /* Extremely high z-index */
        background: rgba(255, 255, 255, 0.98);
        padding: 12px 18px;
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
        border: 2px solid #1f77b4;
        font-family: 'Source Sans Pro', sans-serif;
        display: flex;
        gap: 15px;
        align-items: center;
    }
    .fixed-nav a {
        text-decoration: none;
        color: #1f77b4;
        font-weight: 700;
        font-size: 15px;
        transition: all 0.3s ease;
        padding: 6px 12px;
        border-radius: 6px;
        border: 1px solid transparent;
    }
    .fixed-nav a:hover {
        color: #ffffff;
        background: #1f77b4;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(31, 119, 180, 0.3);
        border-color: #1f77b4;
    }
    .fixed-nav a:active {
        transform: translateY(0);
    }
    /* Ensure nothing covers the navigation */
    .main .block-container {
        padding-top: 70px !important;
    }
    /* Make sure Streamlit elements don't overlap */
    div[data-testid="stSidebar"] {
        z-index: 99999;
    }
    </style>
    
    <div class="fixed-nav">
        <a href="https://github.com/nasirk4/marketing-sentiment-pro" target="_blank" title="Documentation">📖 Docs</a>
        <a href="https://github.com/nasirk4/marketing-sentiment-pro/issues" target="_blank" title="Report Issues">🐛 Issues</a>
        <a href="https://github.com/nasirk4/marketing-sentiment-pro" target="_blank" title="Star on GitHub">⭐ Star</a>
    </div>
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