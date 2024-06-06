import requests
import logging
import aiohttp
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch_sitemap(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                logger.error(f"Failed to fetch sitemap from {url}, status code: {response.status}")
                return None
    except Exception as e:
        logger.error(f"Exception occurred while fetching sitemap from {url}: {e}")
        return None

def parse_sitemap(xml):
    soup = BeautifulSoup(xml, features="xml")  # Use XML parser
    urls = [loc.text for loc in soup.find_all('loc')]
    return urls

async def get_all_sitemap_urls(sitemap_url, session):
    sitemap_content = await fetch_sitemap(session, sitemap_url)
    if sitemap_content:
        urls = parse_sitemap(sitemap_content)
        all_urls = []
        for url in urls:
            if url.endswith('.xml'): 
                all_urls.extend(await get_all_sitemap_urls(url, session))
            else:
                all_urls.append(url)
        return all_urls
    else:
        return []

async def get_sitemap_urls(sitemap_url):
    async with aiohttp.ClientSession() as session:
        all_urls = await get_all_sitemap_urls(sitemap_url, session)
        return all_urls