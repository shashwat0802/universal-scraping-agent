from flask import Flask, request, jsonify
import boto3
import os
import asyncio
import requests
import logging
from dotenv import load_dotenv
from src.browser_based_agent.main import browser_based_agent_function
from src.image_based_agent.main import scrape_website_using_image 
from src.utils.search import take_screenshot
from src.openai.actions import summarize_image , summarize_complete_website 
from src.extract_sitemap.main import get_sitemap_urls
from src.independent_search.main import independent_search

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# AWS S3 configuration
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AWS_REGION = os.getenv('AWS_REGION')
S3_BASE_URL = f'https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/'
WEBHOOK_URL = "https://webhook.site/60baa5f4-e420-4cd5-8e94-47142be51392"

# Initialize S3 client using the "wallex-sentinel" profile
session = boto3.Session(profile_name='wallex-sentinel')
s3_client = session.client('s3', region_name=AWS_REGION)

@app.route('/' , methods=['GET'])
def index():
    response = s3_client.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response['Buckets']]
    return jsonify(bucket_names)
    # return 'Hello, World!'

@app.route('/get-image', methods=['GET'])
def get_image():
    params = request.args.to_dict()
    image_key = '1_acra.pdf'
    try:

        s3_client.head_object(Bucket=AWS_BUCKET_NAME, Key=image_key)

        image_url = f'{S3_BASE_URL}{image_key}'
        params['image_url'] = image_url
    except s3_client.exceptions.NoSuchKey:
        params['error'] = 'Image not found'
    
    return jsonify(params)

@app.route('/save-image', methods=['POST'])
def post_body():
    data = {}
    placeholder_image_path = 'logs/fc.png'
    if os.path.exists(placeholder_image_path):
        s3_key = 'fc.png'
        
        with open(placeholder_image_path, 'rb') as image_file:
            s3_client.upload_fileobj(image_file, AWS_BUCKET_NAME, s3_key)
        
        uploaded_image_url = f'{S3_BASE_URL}{s3_key}'
        
        data['uploaded_image_url'] = uploaded_image_url
    else:
        data['error'] = 'Placeholder image not found'
    return jsonify(data)

@app.route('/summarize-image', methods=['POST'])
async def summarize_image_route():
    data = request.json or {}
    image_url = data.get('image_url')
    try:
        summary = await summarize_image(image_url)
        return jsonify(summary)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred'})

@app.route('/independent-search', methods=['POST'])
async def independent_search_analysis():
    data = request.json or {}
    website_url = data.get('website_url')
    website_url = f"{website_url}/sitemap.xml"
    print(f"Analyzing website: {website_url}")
    try:
        response = await independent_search(website_url)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred'})

@app.route('/browser-based-agent', methods=['POST'])
async def browser_based_agent():
    data = request.json or {}
    company_name = data.get('company_name')
    try:
        # response = await browser_based_agent_function(company_name)
        response = await scrape_website_using_image(company_name)
        return jsonify(response)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred'})
    
@app.route('/webhook' , methods=['POST'])
async def crawl_webhook():
    data = request.json or {}
    main_content = data.get('data')
    data_array = []
    response = {}
    try:
        for value in main_content:
            url = value['metadata']['sourceURL']
            print(f"Taking Screenshot of URL: {url}")
            uuid = await take_screenshot(url)
            image_path = f"logs/{uuid}.png"
            summary = await summarize_image(image_path)
            print(f'summary : {summary}')
            obj = {
                'url': url,
                'image_uuid': uuid,
                'page_details':summary
            }
            data_array.append(obj)

        final_summary = await summarize_complete_website(data)
        response['company_details'] = final_summary
        response['data'] = data_array
        webhook_response = requests.post(WEBHOOK_URL, json=response)
        print(f"Webhook response status: {webhook_response.status_code}")

        return jsonify(response)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred'})    

if __name__ == '__main__':
    app.run(port=8000 ,debug=True)