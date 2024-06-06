from src.extract_sitemap.main import get_sitemap_urls
from src.utils.search import take_screenshot
from src.openai.actions import filter_links
import json

async def independent_search(website_url):
    try:
        urls = await get_sitemap_urls(website_url)
        print(f'URLs: {urls}')
        # if len(urls) > 5:
        #     urls = urls[:5]
        filtered_urls = await filter_links(urls)
        print(f'Filtered URLs: {filtered_urls}')
        filtered_urls =  json.loads(filtered_urls)
        for url in filtered_urls:
            await take_screenshot(url)
    except Exception as e:
        print(f'Error in Independent search: {e}')
        return None