from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os
import asyncio
from playwright.async_api import async_playwright

load_dotenv()

app = FirecrawlApp(api_key=os.getenv('FC_API_KEY'))

async def fc_search(company_name):
    query = f"Find company website for : {company_name}"
    print(f"Query : {query}")
    try:
        search_result = app.search(query, {
            'pageOptions': {
                'onlyMainContent': True,
                'fetchPageContent': True
            },
            'searchOptions': {
                'limit': 1
            }
        })

        if search_result and search_result[0]["metadata"]["sourceURL"]:
            url = search_result[0]["metadata"]["sourceURL"]
            print(f"URL : {url}")
            await take_screenshot(url , company_name)
        else:
            print("No search result found.")
        
        return search_result[0]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

async def take_screenshot(url, file_name):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, timeout=30000)
        
        file_name = f"{file_name}_fc_search.png"
        await page.screenshot(path=f"logs/{file_name}", full_page=True)
        await browser.close()
        
        print("Screenshot saved")


async def save_data_to_s3(file_name):
    print(f"Uploading {file_name} to S3")
    
