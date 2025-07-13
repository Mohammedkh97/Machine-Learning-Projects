# file: schema_extractor.py
from config import get_api_key
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schemas import DocumentSchema
# from config import llm
from load_model import inference
import json

schema_template = """
Your task is to extract all structured data from the provided document.
The document type could be one of the following:
- EMPLOYMENT CONTRACT FULL WORK
- eVisa - Tourism
- eVisa - Employment
- Residence
- Change Status
- Passport
- Healthcare Professional Registration Certificate

Here is the document text:

{extractedData}

Extract the data according to the corresponding fields and return the structured JSON schema.
Start!
"""
# Load environment variables
api_key = get_api_key()

# ============ MODEL SETUP ============ #

llm = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    temperature=0.0,
    max_tokens=1024,
)

schema_prompt = ChatPromptTemplate.from_template(schema_template)
structured_llm = llm.with_structured_output(DocumentSchema)
schema_chain = schema_prompt | structured_llm


def extract_document_schema(
    extracted_text: str,
):  # extracted_text got from the inference function
    return schema_chain.invoke({"extractedData": extracted_text})


def extract_clean_output(q):
    """
    Given a Pydantic model output (q), extract document_type and only the relevant non-null details.
    """
    data = json.loads(q.model_dump_json())
    doc_type = data.get("document_type")

    # Mapping document_type to its corresponding field name in the schema
    doc_type_field_map = {
        "EMPLOYMENT CONTRACT FULL WORK": "contract_details",
        "eVisa - Tourism": "visa_details",
        "eVisa - Employment": "visa_details",
        "Residence": "residence_details",
        "Change Status": "changeStatus_details",
        "Passport": "passport_details",
        "Healthcare Professional Registration Certificate": "healthcare_details",
    }

    # Lookup the relevant section based on doc_type
    relevant_key = doc_type_field_map.get(doc_type)

    if not relevant_key:
        return json.dumps(
            {
                "document_type": doc_type,
                "message": "Unsupported or unknown document type.",
            },
            indent=4,
        )

    relevant_data = data.get(relevant_key)

    if not relevant_data:
        return json.dumps(
            {"document_type": doc_type, "message": f"No data found for {relevant_key}"},
            indent=4,
        )

    # Return the filtered output
    result = {"document_type": doc_type, relevant_key: relevant_data}

    return json.dumps(result, indent=4)


if __name__ == "__main__":

    # url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    # url = "https://americanamc-ammc-develop-21053955.dev.odoo.com/web/content/11760"

    # url = "http://149.102.141.44:8066/web/content/80106",
    url = "https://americanamc-ammc-develop-21331446.dev.odoo.com/web/content/13542"
    # url = []
    employee_id = "12345"

    text = inference(url, employee_id)
    # print(text)
    q = extract_document_schema(str(text))
    print(q)
    # print(extract_clean_output(q))
