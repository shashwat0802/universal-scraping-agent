from src.extract_sitemap.main import get_sitemap_urls
from src.utils.search import take_screenshot
from src.openai.actions import filter_links
from src.openai.actions import summarize_all_images
import json

async def independent_search(website_url):
    try:
        response = {}
        urls = await get_sitemap_urls(website_url)
        # print(f'URLs: {urls}')
        if len(urls) > 5:
            urls = urls[:5]
        # filtered_urls = await filter_links(urls)
        # print(f'Filtered URLs: {filtered_urls}')
        # filtered_urls = json.loads(filtered_urls)

        # s3_image_urls = []
        data_storage = {}
        s3_image_urls = get_url_from_json('data_storage.json', 'urls')
        urls_to_process = []

        if s3_image_urls is None:
            for url in urls:
                image_url = await take_screenshot(url)
                urls_to_process.append(image_url) 
            s3_image_urls = urls_to_process
            data_storage['urls'] = s3_image_urls
            with open('data_storage.json', 'w') as file:
                json.dump(data_storage, file, indent=4)

        print(f'S3 Image URLs: {s3_image_urls}')
        llm_response = await summarize_all_images(s3_image_urls)
        llm_response = json.loads(llm_response)
        response['image_urls'] = s3_image_urls
        response['data'] = llm_response
        return response
    except Exception as e:
        print(f'Error in Independent search: {e}')
        return None
    
def get_url_from_json(file_path, key):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        value = data.get(key)
        
        return value
    except Exception as e:
        print(f'Error reading JSON file: {e}')
        return None