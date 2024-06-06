summarize_image_prompt =  """
                As an onboarding analyst for a fintech company specializing in payments, you must review Website Secreenshot.
                Please summarize:
                    - Company description
                    - Every product or service they are offering
                    - Owner of the company
                    - Company established date
                """

summarize_image_prompt2 =  """
                As an onboarding analyst for a fintech company specializing in payments, you must review Website Screenshot.
                Output the Information in pure JSON format. The JSON should contain only the structured data extracted from the text, with no additional commentary, explanations, or extraneous information. Only output JSON fields that are defined if no value found then remove it from the output.
                Please summarize the Screenshot and make sure to include the following data:
                    - Company description
                    - Every product or service they are offering with exact name
                    - Industry of the company
                    - Every product or service they are offering with exact name
                    - Owner of the company
                    - Company established date
                    - Summary of the Page in under 150 words
                """

final_summarize_all_page_prompt = """
                You are an onboarding analyst for a fintech company and intelligent text extractor and summarizer.
                Output the Information in pure JSON format. The JSON should contain only the structured data extracted from the text, with no additional commentary, explanations, or extraneous information. Only output JSON fields that are defined if no value found then remove it from the output.
                You have access to the summary of all the pages of the company website.
                For the given text/JSON data provide the following details:
                    - Company Name
                    - Company description
                    - Every product or service they are offering with exact name
                    - Types of Products/Services
                    - Categories of Products/Services
                    - Industry of the company
                    - Owner of the company
                    - Company established date                
                """


# Define system message content
system_message = f"""You are an intelligent text extraction and conversion assistant. Your task is to extract structured information 
                    from the given text and convert it into a pure JSON format. The JSON should contain only the structured data extracted from the text, 
                    with no additional commentary, explanations, or extraneous information. 
                    You could encounter cases where you can't find the data of the fields you have to extract or the data will be in a foreign language.
                    Please process the following text and provide the output in pure JSON format with no words before or after the JSON:"""


filter_links_prompt = """
You are an Excellent Web Analyst and Data Extraction Specialist. You have been given a task to filter out the links from the provided array of urls.
Please filter out the links that are not valid as per the use case defined and provide the final list of valid links.
Filter out the links that might contain the following information and ignore irrelevant links:
    - Company Products and Services details
    - Company Contact details
    - Company About Us details
    - Company Team details
    - Company Partners details
    - Company News details
    - Company Blog details
    - Company Career details
    - Company Events details
    - Company Testimonials details
    - Company Awards details
    - Company Clients details
    - Company Gallery details
    - Company FAQ details
    - Company Terms and Conditions details
    - Any other url that might contain the company information

Output the result in pure JSON format. The JSON should contain only the structured data extracted from the text, with no additional commentary, explanations, or extraneous information.
Output JSON should look like : 
{
    "urls": [
        "https://www.example.com",
        "https://www.example.com",
        "https://www.example.com"
    ]
}
"""

# Define user message content
# user_message = f"Extract the following information from the provided Image.
# Information to extract:"