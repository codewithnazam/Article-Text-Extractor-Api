import requests
from bs4 import BeautifulSoup

def extract_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Example: Extract the title of the article
        title = soup.find('h1').text
        return {"title": title}
    except Exception as e:
        return {"error": str(e)}
