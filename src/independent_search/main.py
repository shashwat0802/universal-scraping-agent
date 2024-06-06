from src.extract_sitemap.main import get_sitemap_urls
from src.utils.search import take_screenshot

async def independent_search(website_url):
    try:
        urls =  get_sitemap_urls(website_url)
        if len(urls) > 5:
            urls = urls[:5]
        for url in urls:
            await take_screenshot(url)
    except Exception as e:
        print(f'Error in Independent search: {e}')
        return None