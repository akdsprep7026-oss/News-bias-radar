import streamlit as st
import re


# Import our project modules, including the new advanced bias function
from article_fetcher import fetch_article_data
from analyzer import summarize_text, analyze_sentiment, analyze_bias_advanced
from visualizer import create_sentiment_chart, create_bias_chart

# --- Page Configuration ---
st.set_page_config(
    page_title="Radar | AI News Analysis", 
    page_icon="📡", 
    layout="wide"
)

# --- Custom CSS for Aesthetics ---
st.markdown("""
<style>
    /* Core App Styling */
    .stApp {
        background-color: #1E1E1E;
        color: #EAEAEA;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }

    /* Titles and Headers */
    h1, h2, h3 {
        color: #FFFFFF;
    }

    /* Buttons */
    .stButton>button {
        border: 2px solid #00A8E8;
        border-radius: 20px;
        color: #00A8E8;
        background-color: transparent;
        padding: 10px 24px;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #00A8E8;
        color: #FFFFFF;
        border-color: #00A8E8;
    }
    .stButton>button:focus {
        box-shadow: none !important;
    }

    /* Text Input */
    .stTextInput>div>div>input {
        background-color: #2F2F2F;
        color: #EAEAEA;
        border-radius: 10px;
        border: 1px solid #4F4F4F;
    }

    /* Custom containers/cards */
    .custom-container {
        border-radius: 15px;
        padding: 20px;
        background-color: #2F2F2F;
        border: 1px solid #4F4F4F;
        margin-bottom: 1rem;
    }

    /* Summary blockquote style */
    .summary-quote {
        border-left: 4px solid #00A8E8;
        padding-left: 15px;
        margin-left: 5px;
        font-style: italic;
        color: #C0C0C0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1rem;
        color: #888;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# --- App Header ---
st.markdown("""
<div style="text-align: center;">
    <h1>📡 Radar</h1>
    <p style="color: #00A8E8; font-size: 1.2rem;">AI-Powered News Analysis</p>
</div>
""", unsafe_allow_html=True)
st.divider()


# --- Input Form ---
with st.form(key='url_form'):
    url = st.text_input("Enter the URL of a news article to begin analysis", placeholder="https://www.your-news-article-url.com")
    submit_button = st.form_submit_button(label='Analyze Article ✨')


# --- Analysis and Display Logic ---
if submit_button:
    if not url.strip() or not re.match(r'^https?://', url):
        st.warning("Please enter a valid URL (e.g., starting with http:// or https://).")
    else:
        with st.spinner("Hold tight... Our AI is reading, summarizing, and analyzing the article..."):
            try:
                article = fetch_article_data(url)
                if not article or not article.text:
                    st.error("Failed to retrieve the article. The website might be blocking automated access, or the URL may be incorrect. Please try a different source.")
                else:
                    # Run all analyses, using the new advanced function
                    article_text = article.text
                    summary = summarize_text(article_text)
                    sentiment = analyze_sentiment(article_text)
                    bias = analyze_bias_advanced(article_text) # <-- UPDATED FUNCTION CALL

                    # Create visualizations
                    sentiment_fig = create_sentiment_chart(sentiment)
                    bias_fig = create_bias_chart(bias)
                    
                    st.header(f"Analysis Report: *{article.title}*")

                    # --- Display Results in Tabs ---
                    tab1, tab2, tab3 = st.tabs(["📝 Summary", "🎭 Sentiment", "⚖️ Political Bias"])

                    with tab1:
                        st.markdown('<p class="summary-quote">' + summary + '</p>', unsafe_allow_html=True)

                    with tab2:
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.metric(
                                label="Overall Sentiment", 
                                value=sentiment['label'].capitalize(), 
                                delta=f"{sentiment['score']:.2%} Confidence",
                                delta_color="off"
                            )
                            st.info("Sentiment analysis determines the emotional tone of the text. The score indicates the model's confidence in its classification.")
                        with col2:
                            st.plotly_chart(sentiment_fig, use_container_width=True)

                    with tab3:
                        if bias_fig:
                            # Update the chart title and text for the new scoring method
                            bias_fig.update_layout(title_text='Political Bias Semantic Similarity')
                            st.plotly_chart(bias_fig, use_container_width=True)
                        else:
                            st.success("Our analysis did not detect significant politically-leaning language.")
                        # Update the disclaimer to explain the new method
                        st.warning("Disclaimer: Bias detection is experimental. It measures the semantic similarity of the article's language to core political concepts, not a definitive judgment of bias.")

            except Exception as e:
                st.error(f"An unexpected error occurred during analysis: {e}")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Radar | An AI Experiment in Media Analysis</p>
</div>
""", unsafe_allow_html=True)