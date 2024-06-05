import openai
import base64

def summarize_image(image_path):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content":[
            {
                "type": "text",
                "text": """
                As an onboarding analyst for a fintech company specializing in payments, you must review Website Secreenshoot.
                Please summarize:
                    - Company description
                    - Every product or service they are offering
                    - Owner of the company
                    - Company established date
                """
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