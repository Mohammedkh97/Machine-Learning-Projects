import requests
import json
from load_model import inference
from config import get_api_key


def build_prompt(ocr_text):
    return f"""
Here is some OCR text from a scanned document:

{ocr_text}

Please extract and return this data in JSON format with fields and don't miss to mention the document type:
The document type maybe is passport, visa (tourism or employment), change status, employment contract, residence, healthcare professional
if the document is a passport, extract the following fields:
    {{
    "document_type": "Passport",
    "passport_details": [
        {{
            "passport_number": "",
            "name": "",
            "date_of_birth": "DD/MM/YYYY",
            "date_of_issue": "DD/MM/YYYY",
            "date_of_expiry": "DD/MM/YYYY",
            "profession": ""
        }}
    ]
}}
if the document is a visa, extract the following fields:
{{
"document_type": "Visa - [Tourism or Employment]",
"visa_details": [
{{
        "issue_date": "DD/MM/YYYY",
        "place_of_issue": "",
        "valid_until": "DD/MM/YYYY",
        "uid_number": "",
        "full_name": "",
        "nationality": "",
        "place_of_birth": "",
        "date_of_birth": "DD/MM/YYYY",
        "passport_number": "",
        "profession": ""
    }}
]
}}
if the document is a change status, extract the following fields:
    {{
"document_type": "Change Status",
"change_status_details": [
{{
        "uid_number": "",
        "name": "",
        "nationality": "",
        "passport_number": "",
        "profession": "",
        "employer_name": "",
        "residence_stamping_deadline": "DD/MM/YYYY"
        
    }}
]
}}
if the document is an Employment Contract, extract the following fields which related to the employee:
    {{
"document_type": "Employment contract",
"contract_details": [
    {{
        "work_style": "Full Time or Part Time",
        "transaction_number": "",
        "nationality": "",
        "passport_number": "",
        "date_of_birth": "DD/MM/YYYY",
        "academic_qualification": "",
        "contract_start": "DD/MM/YYYY",
        "contract_end": "DD/MM/YYYY"
    }}
]
}}
if the document is a residence, extract the following fields:
    {{
"document_type": "Residence",
"residence_details": [
{{
        "id_number": "",
        "passport_number": "",
        "name": "",
        "issue_date": "DD/MM/YYYY",
        "expiry_date": "DD/MM/YYYY",
        "profession": ""
    }}
]
}}

if healthcare professional registeration certification, extract the following fields:
{{
"document_type": "Healthcare",
"healthcare_certificate_details": [
{{
        "professional_name": "",
        "dha_unique_id": ""
    }}
]
}}
if tenancty contract information registeration certificate, extract the following fields:

{{
"document_type": "tenancty contract information registeration certificate",
"contract_information_registeration_certificate": [
{{
        "tenant_name": "",
        "property_no": ""
        "start_date":
        "end_date":
        "license_no":
        "registeration_date":
        "expiry_date":
        
    }}
]
}}
    
"""


def extract_document_schema_from_url(url, employee_id):
    ocr_text = inference(url, employee_id)
    prompt = build_prompt(ocr_text)
    api_key = get_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        data=json.dumps(
            {
                "model": "deepseek/deepseek-r1-distill-llama-70b:free",
                "messages": [{"role": "user", "content": prompt}],
            }
        ),
    )

    result = response.json()
    response_text = result["choices"][0]["message"]["content"]
    return response_text


def main():
    pdf_urls = [
        "https://americanamc-ammc-develop-21331446.dev.odoo.com/web/content/13542",
        "http://149.102.141.44:8066/web/content/80106",
        # add more PDF URLs here...
    ]
    employee_id = "12345"
    print(f"Running AI Document Extractor on {len(pdf_urls)} PDF URLs...")
    for pdf_url in pdf_urls:
        schema_json = extract_document_schema_from_url(pdf_url, employee_id)
        print("\nExtracted Schema in JSON Format:\n")
        print(schema_json)


if __name__ == "__main__":
    main()
