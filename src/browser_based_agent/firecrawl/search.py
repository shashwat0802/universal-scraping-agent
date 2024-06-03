from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

app = FirecrawlApp(api_key=os.getenv('FC_API_KEY'))

async def fc_search(company_name):
    query = f"Find company website for : {company_name}"
    
    try:
        search_result = await app.search(query, {
            'pageOptions': {
                'onlyMainContent': True,
                'fetchPageContent': True
            },
            'searchOptions': {
                'limit': 1
            }
        })
        return search_result
    except Exception as e:
        print(f"An error occurred: {e}")
        return None