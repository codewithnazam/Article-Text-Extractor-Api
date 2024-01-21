import requests
from bs4 import BeautifulSoup

def extract_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting the title
        title = soup.find('h1')
        title_text = title.get_text(strip=True) if title else "Title not found"

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
            return False

        # Removing unwanted tags including sidebars
        for tag in main_content.find_all(is_unwanted_tag):
            tag.decompose()

        # Extracting text
        text = ' '.join(main_content.stripped_strings)

      

        return {"title": title_text, "article": text}
    except Exception as e:
        return {"error": str(e)}
