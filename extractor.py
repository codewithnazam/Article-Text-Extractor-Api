# import requests
# from bs4 import BeautifulSoup

# def extract_data(url):
#     try:
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (compatible; YourBot/0.1)'
#         }
#         response = requests.get(url, headers=headers)
#         soup = BeautifulSoup(response.content, 'lxml')

#         # Define a function to get meta content
#         def get_meta_content(attr_name, attr_value):
#             tag = soup.find('meta', attrs={attr_name: attr_value})
#             return tag['content'] if tag and 'content' in tag.attrs else None

#         # Extracting the title from meta tag
#         title_text = get_meta_content('property', 'og:title') or "Title not found"

#            # Extract metadata with simple field names
#         metadata = {
#             'image': get_meta_content('property', 'og:image'),
#             'description': get_meta_content('property', 'og:description'),
#             'author': get_meta_content('name', 'author'),
#             'language': get_meta_content('property', 'og:locale'),
#             'site_name': get_meta_content('property', 'og:site_name'),
#         }

#         # Extract tags
#         tags = {tag.get_text(strip=True) for tag in soup.find_all(class_=lambda v: v and v.startswith('tag'))}
#         metadata['tags'] = list(tags)[:10]

#         main_content = soup.find(['article', 'main', {'role': 'main'}]) or soup

#         # Function to identify unwanted tags
#         def is_unwanted_tag(tag):
#             if tag.name in ['script', 'style', 'header', 'footer', 'aside', 'h1']:
#                 return True
#             if tag.get('id', '').startswith('sidebar') or tag.get('role') in ['navigation', 'widget']:
#                 return True
#             if 'author' in tag.get('class', '') or 'categories' in tag.get('class', '') or 'nv-meta-list' in tag.get('class', '') or 'text-muted' in tag.get('class', ''):
#                 return True
#             if tag.name in ['div', 'span'] and ('author' in tag.get('id', '') or 'category' in tag.get('id', '')):
#                 return True
#             return False

#         # Removing unwanted tags including sidebars and author info
#         for tag in main_content.find_all(is_unwanted_tag):
#             tag.decompose()

#         # Extract text
#         metadata['article'] = ' '.join(main_content.stripped_strings)

#         # Return structured data including title
#         return {"title": title_text, **metadata}
#     except Exception as e:
#         return {"error": str(e)}


import requests
from bs4 import BeautifulSoup

def get_meta_content(soup, attr_name, attr_value):
    tag = soup.find('meta', attrs={attr_name: attr_value})
    return tag['content'] if tag and 'content' in tag.attrs else None

def is_unwanted_tag(tag):
    unwanted_tags = ['script', 'style', 'header', 'footer', 'aside', 'h1']
    unwanted_ids = ['sidebar', 'navigation', 'widget']
    unwanted_classes = ['author', 'categories', 'nv-meta-list', 'text-muted']
    return any([
        tag.name in unwanted_tags,
        tag.get('id', '').startswith(tuple(unwanted_ids)),
        any(cls in tag.get('class', '') for cls in unwanted_classes),
        tag.name in ['div', 'span'] and any(cls in tag.get('id', '') for cls in ['author', 'category'])
    ])

def extract_data(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; YourBot/0.1)'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')

        metadata = {
            'title': get_meta_content(soup, 'property', 'og:title') or "Title not found",
            'image': get_meta_content(soup, 'property', 'og:image'),
            'description': get_meta_content(soup, 'property', 'og:description'),
            'author': get_meta_content(soup, 'name', 'author'),
            'language': get_meta_content(soup, 'property', 'og:locale'),
            'site_name': get_meta_content(soup, 'property', 'og:site_name'),
            'tags': list({tag.get_text(strip=True) for tag in soup.find_all(class_=lambda v: v and v.startswith('tag'))})[:10]
        }

        main_content = soup.find(['article', 'main', {'role': 'main'}]) or soup
        for tag in main_content.find_all(is_unwanted_tag):
            tag.decompose()

        metadata['article'] = ' '.join(main_content.stripped_strings)

        return metadata
    except Exception as e:
        return {"error": str(e)}
