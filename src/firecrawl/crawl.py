from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os
import asyncio
from playwright.async_api import async_playwright

load_dotenv()

app = FirecrawlApp(api_key=os.getenv('FC_API_KEY'))

async def fc_crawl(company_name):
    query = f"Crawling website for URL : {company_name}"
    print(f"Query : {query}")
    try:
        crawl_result = app.crawl_url('mendable.ai', params={
            'crawlerOptions': {
                'limit': 3
            },
            'pageOptions': {
                'onlyMainContent': False
            }
        }, wait_until_done=False)
        
        return crawl_result
    except Exception as e:
        print(f"An error occurred: {e}")
        return None