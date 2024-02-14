# import requests
# from bs4 import BeautifulSoup

# def get_meta_content(soup, attr_name, attr_value):
#     tag = soup.find('meta', attrs={attr_name: attr_value})
#     return tag['content'] if tag and 'content' in tag.attrs else None

# def is_unwanted_tag(tag):
#     unwanted_tags = ['script', 'style', 'header', 'footer', 'aside', 'h1']
#     unwanted_ids = ['sidebar', 'navigation', 'widget']
#     unwanted_classes = ['author', 'categories', 'nv-meta-list', 'text-muted', 'event-promo', 'social-share', 'speechify-ignore']
#     return any([
#         tag.name in unwanted_tags,
#         tag.get('id', '').startswith(tuple(unwanted_ids)),
#         any(cls in tag.get('class', '') for cls in unwanted_classes),
#         tag.name in ['div', 'span'] and any(cls in tag.get('id', '') for cls in ['author', 'category'])
#     ])

# def extract_data(url):
#     try:
#         headers = {'User-Agent': 'Mozilla/5.0 (compatible; YourBot/0.1)'}
#         response = requests.get(url, headers=headers)
#         soup = BeautifulSoup(response.content, 'lxml')

#         metadata = {
#             'title': get_meta_content(soup, 'property', 'og:title') or "Title not found",
#             'image': get_meta_content(soup, 'property', 'og:image'),
#             'description': get_meta_content(soup, 'property', 'og:description'),
#             'author': get_meta_content(soup, 'name', 'author'),
#             'language': get_meta_content(soup, 'property', 'og:locale'),
#             'site_name': get_meta_content(soup, 'property', 'og:site_name'),
#             'tags': list({tag_class.replace('tag-', '').replace('-', ' ') for tag in soup.find_all(class_=lambda v: v and v.startswith('tag')) for tag_class in tag.get('class')})[:10]
#         }

#         main_content = soup.find(['article', 'main', 'article-body', {'role': 'main'}]) or soup
#         for tag in main_content.find_all(is_unwanted_tag):
#             tag.decompose()

#         metadata['article'] = ' '.join(main_content.stripped_strings)

#         return metadata
#     except Exception as e:
#         return {"error": str(e)}

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
        if article.download_state != 2:  # Check if download was successful
            raise Exception("Failed to download article")

        # Parse the article
        article.parse()

        # Perform NLP to get keywords and summary
        article.nlp()
        
       
        # Compile extracted data
        data = {
            "title": article.title,
            "authors": article.authors,
            "text": article.text,
            "top_image": article.top_image,
            "keywords": article.keywords,
            "summary": article.summary,
            "language": article.meta_lang,
            "description": article.meta_description,
            "article_url": url,  # Added the article URL
        }

        return data
    except Exception as e:
        return {"error": f"Error extracting data: {str(e)}"}

