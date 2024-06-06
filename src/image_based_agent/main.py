import asyncio
from src.utils.search import fc_search 
from src.utils.crawl import fc_crawl 
from src.openai.actions import summarize_image

async def scrape_website_using_image(company_name):
    try:
        print(f"Searching for {company_name}")
        search_result = await fc_search(company_name)
        crawl_result = await fc_crawl(search_result["metadata"]["sourceURL"])
        response = search_result
        response['crawl_result'] = crawl_result
        # image_path = f"logs/{company_name}_fc_search.png"
        # summary = summarize_image(image_path)
        # response['summary'] = summary
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
async def screenshot_every_page(site_map):
    try:
        print(f"Site map with urls : {site_map}")
        for value in site_map:
            print(value)

    except Exception as e:
        print(f"An error occurred: {e}")
        return None