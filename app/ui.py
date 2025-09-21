# 🎨 Streamlit UI components
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from app.logic import analyze_query
from app.config import MAX_TWEETS_DEMO
import os

# ADD THIS IMPORT - crucial for rate limiting
from app.twitter import api_state

def render_sidebar():
    """Renders the configuration sidebar."""
    with st.sidebar:
        st.image("assets/logo.png", width=150) if os.path.exists("assets/logo.png") else st.header("🔍 Sentiment Pro")
        st.header("Configuration Panel")
        
        analysis_mode = st.radio("Analysis Mode", ("Keyword/Hashtag", "User Timeline"))
        query_label = "Search Query" if analysis_mode == "Keyword/Hashtag" else "Twitter @Username"
        query_help = "E.g., #ProductLaunch" if analysis_mode == "Keyword/Hashtag" else "Without the '@' symbol, e.g., 'Google'"
        query = st.text_input(query_label, "AI", help=query_help)
        
        tweet_count = st.slider("Tweets to Analyze", 10, MAX_TWEETS_DEMO, 50, help=f"Demo limited to {MAX_TWEETS_DEMO} tweets.")
        include_retweets = st.checkbox("Include Retweets", value=False)
        
        # ADD DEMO MODE TOGGLE - essential for rate limit control
        demo_mode = st.checkbox("🎭 Use Demo Mode (Recommended)", value=True, 
                               help="Use high-quality sample data to avoid API rate limits")
        
        if st.button("Analyze Sentiment", type="primary", use_container_width=True):
            # SET DEMO MODE STATE - critical for preventing rate limits
            api_state.demo_mode = demo_mode
            st.session_state.force_demo = demo_mode  # Sync with main app state
            st.session_state['analyze_triggered'] = True
            st.session_state['current_query'] = query
            st.session_state['demo_mode'] = demo_mode
        else:
            if 'analyze_triggered' not in st.session_state:
                st.session_state['analyze_triggered'] = False
                
        _render_production_teaser()
        
        return query, analysis_mode, tweet_count, include_retweets

def _render_production_teaser():
    """Renders the expandable section for production features."""
    st.sidebar.markdown("---")
    with st.sidebar.expander("🚀 **Production Ready Features**"):
        st.markdown("""
        **This demo shows core functionality. A production plan unlocks:**
        - 📈 **Historical Trends & Dashboards**
        - 🤖 **Competitor Comparison**
        - 🔔 **Real-time Alerts (Slack/Email)**
        - 📊 **Scheduled PDF Reports**
        - 🗄️ **Data Warehouse Integration**
        - ↗️ **Higher API Limits & Data Sources**
        
        *Fully containerized and deployable in your cloud environment.*
        """)

def render_main_content(df, query, mode):
    """Renders the main content area with analysis results."""
    if df.empty:
        st.warning("No data retrieved or all tweets were filtered out. Try a different query or including retweets.")
        return
        
    # ADD API STATUS INDICATOR - important for user feedback
    from app.twitter import get_api_status
    api_status = get_api_status()
    
    if st.session_state.get('demo_mode', True):
        st.info("🎭 **Demo Mode**: Showing high-quality sample data (no API calls)")
    elif api_status['rate_limited']:
        remaining = int(api_status['rate_limit_remaining'])
        st.warning(f"⏳ **Rate Limited**: Using demo data for {remaining} seconds")
    else:
        st.success("✅ **Live API**: Using real Twitter data")
    
    st.success(f"Analysis complete for **'{query}'**! Processed **{len(df)}** posts.")
    _render_kpi_metrics(df)
    _render_tabs(df)

def _render_kpi_metrics(df):
    """Renders the top KPI metric cards."""
    pos_count = (df['Sentiment'] == 'Positive').sum()
    neg_count = (df['Sentiment'] == 'Negative').sum()
    pos_perc = round(pos_count / len(df) * 100, 1)
    neg_perc = round(neg_count / len(df) * 100, 1)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Samples", len(df))
    m2.metric("Positive", f"{pos_perc}%", f"{pos_count} posts")
    m3.metric("Neutral", f"{round(100 - pos_perc - neg_perc, 1)}%")
    m4.metric("Negative", f"{neg_perc}%", delta_color="inverse")

def _render_tabs(df):
    """Renders the analysis results in separate tabs."""
    tab1, tab2, tab3 = st.tabs(["📊 Sentiment", "☁️ Word Cloud", "📋 Sample Data"])
    
    with tab1:
        fig, ax = plt.subplots()
        df['Sentiment'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax, colors=['#4CAF50','#FFC107','#F44336'])
        ax.set_ylabel('')
        st.pyplot(fig)
    
    with tab2:
        all_words = ' '.join(df['Cleaned_Tweet'])
        if all_words.strip():
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_words)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis('off')
            st.pyplot(fig)
        else:
            st.info("Not enough text to generate a word cloud.")
    
    with tab3:
        st.dataframe(df[['Analysis_Time', 'Sentiment', 'Polarity', 'Raw_Tweet']].style.background_gradient(subset=['Polarity'], cmap='RdYlGn'), width='stretch')

def render_ui():
    """Main function to render the entire UI."""
    st.title("📈 Marketing Sentiment Pro")
    st.markdown("A **DevOps-powered** marketing intelligence tool for real-time social sentiment analysis.")
    
    query, mode, count, include_rt = render_sidebar()
    
    if st.session_state.get('analyze_triggered', False):
        df = analyze_query(mode, query, count, include_rt)
        render_main_content(df, query, mode)