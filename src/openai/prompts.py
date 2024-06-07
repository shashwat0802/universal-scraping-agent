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

final_summarize_all_page_prompt = """
You will be analyzing a company's website screenshot to determine its business activity and assess several risk factors. Follow these steps to complete the task:
Carefully examine the provided screenshot of the company's website.
Identify the primary business activity of the company from the website. Provide a brief summary of the company's business activity.

Check if the company is involved in any prohibited or high-risk industries listed below:
Prohibited Industries:

Auction Houses
Casino (Prohibited for Non-FATF member jurisdictions)
Digital Payment Service Provider (Prohibited for Non-FATF member jurisdictions)
Embassies, Foreign Consulates or Missions
Extractive industries
Gambling Businesses / Junket Operator
Holdmail Services
Illegal Activities / Businesses
Modern Weaponry Businesses / Companies
Multi-level Marketing Companies
Non-Profit Organisations / Non-Governmental Organisations / Religious Charities or Institutions (Prohibited for Non-FATF member jurisdictions)
Pawnshops (Prohibited for Non-FATF member jurisdictions)
Ponzi Schemes / Get-Rich-Quick Schemes
Precious Stones, Metal, Art, Jewellery, Antique Dealers, High-Value Items (Prohibited for Non-FATF member jurisdictions)
Production or Wholesale Trading of Nuclear related Raw Materials, Products and Services
Terrorists or Terrorist Groups
Vice-Related Businesses
High-Risk Industries:
Affiliate Marketing Schemes
Automobile, Boat and Plane Dealerships
Banks (Entities licensed in non-FATF members jurisdictions)
Cash-Intensive Businesses
Casino (Entities licensed in FATF members jurisdictions)
Commodity Trading Associated with High-Risk Products (e.g., Oil, Metals, Gold, Silver, Copper, Chemical, Aluminium)
Digital Payment Service Provider (Restricted to FX conversion on first-party basis and entities licensed in FATF member jurisdictions)
E-Commerce (Online Retailer)
Exempted Payment Service Providers
Finance Companies (Entities licensed in non-FATF members jurisdictions)
Import and Export
Maritime / Shipping
Moneylending Business
Nightlife Establishments / Spa Services
Non-Profit Organisations / Non-Governmental Organisations / Religious Charities or Institutions (Entities licensed in FATF members jurisdictions)
Offshore Banks
Oil & Gas
Online Marketplace
Pawnshops (Entities licensed in FATF member jurisdictions)
Payment Services Provider / Remittance Services / Money Service Businesses / Stored Value Facility Holders (Entities licensed in non-FATF members jurisdictions)
Precious Stones, Metal, Art, Jewellery, Antique Dealers, High-Value Items (Entities licensed in FATF members jurisdictions)
Real-Estate
Trust and Corporate Service Providers
Unregulated Businesses
Vacation Rental Properties / Sites
Wholesale Trading Associated with High-Risk Products (e.g., Oil, Metals, Gold, Silver, Copper, Chemical, Aluminium)

Determine if the company is operating in any of the prohibited or high-risk countries based on the list below:

Prohibited Countries:
Afghanistan, Montenegro, Albania, Nicaragua, Belarus, North Korea, Bosnia and Herzegovina, Republic of North Macedonia, Central African Republic, Russia, Cuba, Serbia, Democratic Republic of Congo, Somalia, Ethiopia, South Sudan, Iran, Sudan, Iraq, Syria, Kosovo, Ukraine, Lebanon, Venezuela, Libya, Yemen, Mali, Zimbabwe
High-Risk Countries:
American Samoa, Guinea-Bissau, Angola, Haiti, Anguilla, Jamaica, Antigua and Barbuda, Kyrgyzstan, Azerbaijan, Mozambique, Bahamas, Myanmar, Bangladesh, Nigeria, Barbados, Palau, Belize, Panama, Bolivia, Philippines, Bulgaria, Samoa, Burkina Faso, Senegal, Burundi, Seychelles, Cambodia, Sierra Leone, Cameroon, South Africa, Chad, Tajikistan, Comoros, Tanzania, Congo, Trinidad and Tobago, Croatia, Turkey, Djibouti, Turkmenistan, Egypt, Turks and Caicos Islands, Equatorial Guinea, Uganda, Eritrea, United Arab Emirates, Fiji, United States Virgin Islands, Gibraltar, Vanuatu, Guam, Vietnam, Guatemala, West Bank and Gaza, Guinea
Check if the company is dealing in dual-use goods, which are products that can be used for both civilian and military purposes.
Look for any indications that the company website might be a dummy website, such as very little content, broken links, or lack of contact information.
Identify the countries in which the company is operating. This information can often be found in sections like "Contact," "Locations," or "Global Presence."
Check if the company name on the screenshot matches the customer's company name in Chinese or English.

Output the result in pure JSON format. The JSON should contain only the structured data extracted from the text, with no additional commentary, explanations, or extraneous information.
Output JSON should look like : 

{output_schema}

"""

output_schema = {
    "Company Business Activity": "",
    "Is the Company dealing in any prohibited or high-risk industries": "",
    "If YES, specify which industries": "",
    "Is the Company operating in any of the prohibited or high-risk countries": "",
    "If YES, specify which countries": "",
    "Is the Company dealing in product that is dual-use goods": "",
    "Is there indication that the Company website might be a dummy website": "",
    "What are the countries that the Company is operating in": "",
    "Is the Company name on the URL same as the customer's company name in Chinese or English": "",
    "If NO, specify the differences": "",
    "List of Products/Services": "",
}