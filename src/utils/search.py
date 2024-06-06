from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os
import asyncio
from playwright.async_api import async_playwright
import uuid
import boto3

load_dotenv()

# AWS S3 configuration
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AWS_REGION = os.getenv('AWS_REGION')
S3_BASE_URL = f'https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/'
app = FirecrawlApp(api_key=os.getenv('FC_API_KEY'))

# Initialize S3 client using the "wallex-sentinel" profile
session = boto3.Session(profile_name='wallex-sentinel')
s3_client = session.client('s3', region_name=AWS_REGION)

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
            await take_screenshot(url)
        else:
            print("No search result found.")
        
        return search_result[0]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

async def take_screenshot(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, timeout=30000)
        screenshot_uuid = uuid.uuid4().hex
        file_name = f"{screenshot_uuid}.png"
        await page.screenshot(path=f"logs/{file_name}", full_page=True)
        s3_image_url = await save_data_to_s3(file_name)
        await browser.close()
        print("Screenshot saved")
        return s3_image_url


async def save_data_to_s3(file_name):
    try : 
        print(f"Uploading {file_name} to S3")
        image_path = f'logs/{file_name}'
        if os.path.exists(image_path):
            s3_key = '2_acra.pdf'
            with open(image_path, 'rb') as image_file:
                s3_client.upload_fileobj(image_file, AWS_BUCKET_NAME, s3_key)
            uploaded_image_url = f'{S3_BASE_URL}{s3_key}'
            os.remove(image_path)
            print(f"Deleted local file {file_name} after upload")
        return uploaded_image_url
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
