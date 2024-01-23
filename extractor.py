import requests
from bs4 import BeautifulSoup

def extract_data(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; YourBot/0.1)'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')

        # Define a function to get meta content
        def get_meta_content(attr_name, attr_value):
            tag = soup.find('meta', attrs={attr_name: attr_value})
            return tag['content'] if tag and 'content' in tag.attrs else None

        # Extracting the title from meta tag
        title_text = get_meta_content('property', 'og:title') or "Title not found"

           # Extract metadata with simple field names
        metadata = {
            'image': get_meta_content('property', 'og:image'),
            'description': get_meta_content('property', 'og:description'),
            'author': get_meta_content('name', 'author'),
            'language': get_meta_content('property', 'og:locale'),
            'site_name': get_meta_content('property', 'og:site_name'),
        }

        # Extract tags
        tags = {tag.get_text(strip=True) for tag in soup.find_all(class_=lambda v: v and v.startswith('tag'))}
        metadata['tags'] = list(tags)[:10]

        main_content = soup.find(['article', 'main', {'role': 'main'}]) or soup

        # Function to identify unwanted tags
        def is_unwanted_tag(tag):
            if tag.name in ['script', 'style', 'header', 'footer', 'aside', 'h1']:
                return True
            if tag.get('id', '').startswith('sidebar') or tag.get('role') in ['navigation', 'widget']:
                return True
            if 'author' in tag.get('class', '') or 'categories' in tag.get('class', '') or 'nv-meta-list' in tag.get('class', '') or 'text-muted' in tag.get('class', ''):
                return True
            if tag.name in ['div', 'span'] and ('author' in tag.get('id', '') or 'category' in tag.get('id', '')):
                return True
            return False

        # Removing unwanted tags including sidebars and author info
        for tag in main_content.find_all(is_unwanted_tag):
            tag.decompose()

        # Extract text
        metadata['article'] = ' '.join(main_content.stripped_strings)

        # Return structured data including title
        return {"title": title_text, **metadata}
    except Exception as e:
        return {"error": str(e)}
