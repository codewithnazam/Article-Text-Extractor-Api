import requests
from bs4 import BeautifulSoup

def extract_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting the title
        title = soup.find('h1')
        title_text = title.get_text(strip=True) if title else "Title not found"

      # Extracting metadata from 'meta' tags
        def get_meta_content(attr_name, attr_value):
            tag = soup.find('meta', attrs={attr_name: attr_value})
            return tag['content'] if tag and 'content' in tag.attrs else None

        main_image = get_meta_content('property', 'og:image')
        description = get_meta_content('property', 'og:description')
        author = get_meta_content('name', 'author')  # Updated to correctly target 'name' attribute
        language = get_meta_content('property', 'og:locale')
        site_name = get_meta_content('property', 'og:site_name')

        # Extracting tags
        tags = set()
        for element in soup.find_all(True, class_=lambda value: value and value.startswith('tag')):
            for class_name in element.get('class', []):
                if class_name.startswith('tag'):
                    cleaned_tag = class_name.replace('tag-', '').replace('-', ' ')
                    tags.add(cleaned_tag)
        tags = list(tags)[:10]  # Limit to 10 tags

        # Finding the main content container
        main_content = soup.find(['article', 'main', {'role': 'main'}])
        if not main_content:
            main_content = soup
        

        # Function to identify unwanted tags
        def is_unwanted_tag(tag):
            if tag.name in ['script', 'style', 'header', 'footer', 'aside']:
                return True
            if tag.get('id', '').startswith('sidebar'):
                return True
            if tag.get('role') in ['navigation', 'widget']:
                return True
            if 'author' in tag.get('class', '') or 'categories' in tag.get('class', ''):
                return True
            if tag.name in ['div', 'span'] and ('author' in tag.get('id', '') or 'category' in tag.get('id', '')):
                return True
            return False

        # Removing unwanted tags including sidebars
        for tag in main_content.find_all(is_unwanted_tag):
            tag.decompose()

        # Extracting text
        text = ' '.join(main_content.stripped_strings)

      

        return {
            "title": title_text,
            "article": text,
            "image": main_image,
            "description": description,
            "author": author,
            "language": language,
            "site_name": site_name,
            "tags": tags
        }
    except Exception as e:
        return {"error": str(e)}
