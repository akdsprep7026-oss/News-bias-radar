# Importing the necessary classes from the newspaper library
from newspaper import Article, Config
from newspaper.article import ArticleException

def fetch_article_data(url):
    """
    Fetches, downloads, and parses an article from a given URL,
    using a custom user-agent to avoid being blocked.
    
    Args:
        url (str): The URL of the news article.
        
    Returns:
        newspaper.Article: An Article object with parsed data, or None if an error occurs.
    """
    try:
        # Creating a configuration object to customize requests
        config = Config()
        
        # Setting a realistic browser user-agent to mimic a real browser
        config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        
        # Setting a timeout for requests to prevent the script from hanging
        config.request_timeout = 15

        # Instantiating the Article object with the URL and our custom configuration
        article = Article(url, config=config)

        # Downloading the article's HTML. This is the step that can fail.
        article.download()

        # Parsing the downloaded HTML to extract the main content
        article.parse()

        # Using newspaper's built-in NLP to pre-process for keywords and summary
        article.nlp()

        # If all steps succeed, returning the processed article object
        return article

    except ArticleException as e:
        # If newspaper3k fails at any step, catching the error and printing a message
        print(f"Error: Could not fetch or parse the article from {url}.")
        print(f"Details: {e}")
        return None

# This block of code only runs when you execute the script directly
if __name__ == "__main__":
    # A working URL from the Times of India
    sample_url = "https://timesofindia.indiatimes.com/city/dehradun/705-deaths-in-10-yrs-multiple-studies-warn-of-flash-floods-emerging-as-major-killer-in-ukhand/articleshow/123206705.cms"
    
    print(f"Attempting to fetch article from: {sample_url}\n")
    
    # Calling our main function
    news_article = fetch_article_data(sample_url)
    
    # Only printing the details if the article was fetched successfully
    if news_article:
       
        print("--- Article Fetched Successfully! ---\n")
        
        print(f"Title: {news_article.title}\n")
        print(f"Authors: {', '.join(news_article.authors)}\n")
        print(f"Publication Date: {news_article.publish_date}\n")
        
        print("--- Article Text (first 300 characters) ---")
        print(f"{news_article.text[:300]}...\n")
        
        print("--- Article Summary (from newspaper3k's algorithm) ---")
        print(f"{news_article.summary}\n")
        
        print("----------------------------------------")
