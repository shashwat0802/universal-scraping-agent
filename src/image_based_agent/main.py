import asyncio
from src.firecrawl.search import fc_search 
from src.firecrawl.crawl import fc_crawl 
from src.openai.actions import summarize_image

async def scrape_website_using_image(company_name):
    try:
        print(f"Searching for {company_name}")
        search_result = await fc_search(company_name)
        crawl_result = await fc_crawl(search_result[0]["metadata"]["sourceURL"])
        image_path = f"logs/{company_name}_fc_search.png"
        summary = summarize_image(image_path)
        search_result['summary'] = summary
        return search_result
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