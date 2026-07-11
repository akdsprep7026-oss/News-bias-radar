# Importing our custom functions
from article_fetcher import fetch_article_data
from analyzer import summarize_text, analyze_sentiment, analyze_bias
from visualizer import create_sentiment_chart, create_bias_chart # Import new functions


if __name__ == "__main__":
    sample_url = "https://timesofindia.indiatimes.com/city/dehradun/705-deaths-in-10-yrs-multiple-studies-warn-of-flash-floods-emerging-as-major-killer-in-ukhand/articleshow/123206705.cms"
    
    # 1. Fetching the article
    print("--- Step 1: Fetching Article ---")
    news_article = fetch_article_data(sample_url)
    print("--------------------------------\n")

    if news_article:
        article_text = news_article.text
        
        # 2. Summarizing the text
        print("--- Step 2: Generating Advanced Summary ---")
        advanced_summary = summarize_text(article_text)
        print("-------------------------------------------\n")

        # 3. Analyzing Sentiment and Bias
        print("--- Step 3: Performing Analysis ---")
        sentiment = analyze_sentiment(article_text)
        bias = analyze_bias(article_text)
        print("-----------------------------------\n")

        # 4. Generating and saving visualizations
        print("--- Step 4: Generating Visualizations ---")
        create_sentiment_chart(sentiment)
        create_bias_chart(bias)
        print("-----------------------------------------\n")
        
        # 5. Displaying text report in console
        print("========== Full Analysis Report ==========\n")
        # ... (The rest of the print statements are the same)
        print(f"URL: {sample_url}\n")
        print(f"Title: {news_article.title}\n")
        
        print("--- Sentiment ---")
        print(f"Label: {sentiment['label']}, Score: {sentiment['score']:.4f}\n")
        
        print("--- Political Bias (Lexicon-Based) ---")
        print(f"Left-Leaning Word Count: {bias['left_leaning_score']}")
        print(f"Right-Leaning Word Count: {bias['right_leaning_score']}\n")
        
        print("--- Summaries ---")
        print(">>> Original Summary (newspaper3k):")
        print(news_article.summary)
        print("\n>>> Advanced Summary (Transformer):")
        print(advanced_summary)
        
        print("\n==========================================")
