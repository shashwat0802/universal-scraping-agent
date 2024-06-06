import openai
import base64
import os
import asyncio
from src.openai.prompts import filter_links_prompt , summarize_image_prompt2 , final_summarize_all_page_prompt

openai.api_key = os.getenv('OPENAI_API_KEY')

async def summarize_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            response_format={ "type": "json_object" },
            messages=[
            {
                "role": "user",
                "content":[
                {
                    "type": "text",
                    "text": summarize_image_prompt2
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
                ]
            }]
        )
        print(response.usage)
        summary = response.choices[0].message.content
        print(f'page summary : {summary}')
        return summary
    except Exception as e:
        print(f'Error in Open AI summarize image : {e}')
        return None
    
async def summarize_complete_website(final_response):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            response_format={ "type": "json_object" },
            messages=[
                {
                    "role": "system",
                    "content":[
                    {
                        "type": "text",
                        "text": final_summarize_all_page_prompt
                    },
                    ]
                },
                {
                    "role": "user",
                    "content":[
                    {
                        "type": "text",
                        "text": str(final_response)
                    },
                    ]
                }
            ]
        )
        print(response.usage)
        summary = response.choices[0].message.content
        print(f'Complete summary : {summary}')
        return summary
    except Exception as e:
        print(f'Error in Open AI summarize complete website : {e}')
        return None
    
async def filter_links(urls):
    urls_string = "\n".join(urls)
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            response_format={ "type": "json_object" },
            messages=[
                {
                    "role": "system",
                    "content":[
                    {
                        "type": "text",
                        "text": filter_links_prompt
                    },
                    ]
                },
                {
                    "role": "user",
                    "content":[
                    {
                        "type": "text",
                        "text": urls_string
                    },
                    ]
                },
            ]
        )
        print(response.usage)
        urls = response.choices[0].message.content
        return urls
    except Exception as e:
        print(f'Error in Open AI summarize complete website : {e}')
        return None