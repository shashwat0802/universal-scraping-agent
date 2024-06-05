import openai
import base64
import os
import asyncio
from src.openai.prompts import summarize_image_prompt , summarize_image_prompt2

openai.api_key = os.getenv('OPENAI_API_KEY')

async def summarize_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{
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
        return summary
    except Exception as e:
        print(f'Error in Open AI summarize image : {e}')
        return None