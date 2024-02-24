import requests
from newspaper import Article
import validators

def extract_data(url):
    # Validate URL
    if not validators.url(url):
        return {"error": "Please enter a valid URL."}

    try:
        # Initialize the article using Newspaper3k
        article = Article(url)

        # Download the article
        article.download()

        # Check if download was successful
        if article.download_state != 2:
            return {"error": "Failed to download the article. The content might not be accessible or the URL is incorrect."}

        # Parse the article
        article.parse()

        # Sometimes, articles have no text. Check this before proceeding.
        if not article.text:
            return {"error": "No content found in the article."}

        # Perform NLP to get keywords and summary
        article.nlp()

        # Compile extracted data
        data = {
            "title": article.title or "Title not available",
            "authors": article.authors,
            "text": article.text,
            "top_image": article.top_image or "No image available",
            "keywords": article.keywords,
            "summary": article.summary or "Summary not available",
            "language": article.meta_lang or "Language not detected",
            "description": article.meta_description or "No description available",
            "article_url": url,  # Added the article URL
        }

        return data
    except requests.exceptions.RequestException as e:
        # This catches errors like connectivity issues, timeout, etc.
        return {"error": f"Network error occurred: {str(e)}"}
    except Exception as e:
        # Catch-all for any other exceptions
        return {"error": f"An unexpected error occurred: {str(e)}"}
