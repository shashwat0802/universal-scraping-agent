import requests
import logging
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_sitemap_urls(sitemap_url):
    try:
        page = requests.get(sitemap_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        urls = soup.find_all('loc')
        for url in urls:
            current_url = url.get_text()
            if('.pdf' not in current_url):
                page = requests.get(current_url)
                soup = BeautifulSoup(page.content, 'html.parser')
                title = soup.find('title')
                print(f"Title: {title.get_text()}")
        return urls
    except Exception as e:
        logger.error(f"An error occurred while fetching sitemap: {e}")
        return None