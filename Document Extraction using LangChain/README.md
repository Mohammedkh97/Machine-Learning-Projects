### Document Extraction with LangChain:

Building a full LangChain project for document extraction is a very powerful use case — and fits perfectly with your goal (PDF → JSON structured data, classified by type).
Since you already have clear document types & target schemas — you are 70% ready. 🚀

---

### 🔸 Project Architecture

```
langchain_doc_extractor/
├── data/                      # Input PDFs
├── outputs/                   # JSON output
├── schemas.py                 # Pydantic schemas
├── langchain_pipeline.py      # Main processing script
├── requirements.txt           # Dependencies
└── README.md
```
---


🚀 1️⃣ Use Pydantic for schemas
Pydantic is the Python standard for defining data schemas with validation.
You define models for each document type → LLM generates JSON → Pydantic validates and loads → no errors, structured output.


Great choice — using **Groq** will give you low-latency & cost-effective LLM calls.

---

### ⚙️ Full LangChain Project Example with Groq

(PDF → classify document → parse structured fields → JSON → Pydantic → save)

---

### 🔸 Project Structure

```
langchain_doc_extractor/
├── data/                      # Input PDFs
├── outputs/                   # JSON output
├── schemas.py                 # Pydantic schemas
├── langchain_pipeline.py      # Main processing script
├── requirements.txt           # Dependencies
└── README.md
```

---

### 🔸 1️⃣ `requirements.txt`

```txt
langchain
langchain_groq
langchain-community
langchain-text-splitters
langchain-pydantic
groq
PyMuPDF
pydantic
```

---

### 🔸 2️⃣ `schemas.py`

```python
from pydantic import BaseModel
from typing import List, Literal

# ----- Passport -----
class PassportDetail(BaseModel):
    passport_number: str
    name: str
    date_of_birth: str
    date_of_issue: str
    date_of_expiry: str
    profession: str

class PassportDocument(BaseModel):
    document_type: Literal["Passport"]
    passport_details: List[PassportDetail]

# ----- Visa -----
class VisaDetail(BaseModel):
    issue_date: str
    place_of_issue: str
    valid_until: str
    uid_number: str
    full_name: str
    nationality: str
    place_of_birth: str
    date_of_birth: str
    passport_number: str
    profession: str

class VisaDocument(BaseModel):
    document_type: Literal["Visa - Tourism", "Visa - Employment"]
    visa_details: List[VisaDetail]

# ----- Change Status -----
class ChangeStatusDetail(BaseModel):
    uid_number: str
    name: str
    nationality: str
    passport_number: str
    profession: str
    employer_name: str
    residence_stamping_deadline: str

class ChangeStatusDocument(BaseModel):
    document_type: Literal["Change Status"]
    change_status_details: List[ChangeStatusDetail]

# ----- Employment Contract -----
class ContractDetail(BaseModel):
    work_style: str
    transaction_number: str
    nationality: str
    passport_number: str
    date_of_birth: str
    academic_qualification: str
    contract_start: str
    contract_end: str

class EmploymentContractDocument(BaseModel):
    document_type: Literal["Employment contract"]
    contract_details: List[ContractDetail]

# ----- Residence -----
class ResidenceDetail(BaseModel):
    id_number: str
    passport_number: str
    name: str
    issue_date: str
    expiry_date: str
    profession: str

class ResidenceDocument(BaseModel):
    document_type: Literal["Residence"]
    residence_details: List[ResidenceDetail]

# ----- Healthcare -----
class HealthcareCertificateDetail(BaseModel):
    professional_name: str
    dha_unique_id: str

class HealthcareDocument(BaseModel):
    document_type: Literal["Healthcare"]
    healthcare_certificate_details: List[HealthcareCertificateDetail]
```

---

### 🔸 3️⃣ `langchain_pipeline.py`

```python
import os
import json
import glob
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyMuPDFLoader
from schemas import *

# CONFIG
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # or set manually
INPUT_FOLDER = "data/"
OUTPUT_FOLDER = "outputs/"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# LLM: Groq with Mixtral-8x7b or LLaMA3
llm = ChatGroq(model_name="mixtral-8x7b-32768", temperature=0)

# PROMPT TEMPLATE
template = """
You are an expert document parser.

Document types you know:
- Passport
- Visa - [Tourism or Employment]
- Change Status
- Employment Contract
- Residence
- Healthcare

Based on this document content, first decide the document type, then extract fields as structured JSON using the correct schema.

Return only the final JSON. Do not explain.

Document content:
-------------------
{document_text}
-------------------
"""

# PROCESS FILES
pdf_files = glob.glob(os.path.join(INPUT_FOLDER, "*.pdf"))
print(f"Found {len(pdf_files)} PDF files to process...")

for pdf_path in pdf_files:
    print(f"\nProcessing: {pdf_path}")
    
    # Load PDF
    loader = PyMuPDFLoader(pdf_path)
    pages = loader.load()
    document_text = "\n".join([p.page_content for p in pages])

    # Build prompt
    prompt = PromptTemplate.from_template(template)
    final_prompt = prompt.format(document_text=document_text)

    # Run LLM
    response = llm.invoke(final_prompt)
    llm_output = response.content
    
    # Parse with Pydantic
    data = json.loads(llm_output)
    doc_type = data.get("document_type", "")

    try:
        if "Visa" in doc_type:
            obj = VisaDocument.model_validate(data)
        elif "Passport" in doc_type:
            obj = PassportDocument.model_validate(data)
        elif "Change Status" in doc_type:
            obj = ChangeStatusDocument.model_validate(data)
        elif "Employment contract" in doc_type:
            obj = EmploymentContractDocument.model_validate(data)
        elif "Residence" in doc_type:
            obj = ResidenceDocument.model_validate(data)
        elif "Healthcare" in doc_type:
            obj = HealthcareDocument.model_validate(data)
        else:
            raise ValueError(f"Unknown document type: {doc_type}")

        # Save JSON
        filename = os.path.basename(pdf_path).replace(".pdf", ".json")
        output_path = os.path.join(OUTPUT_FOLDER, filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(obj.model_dump_json(indent=4))

        print(f"✅ Saved output to {output_path}")

    except Exception as e:
        print(f"❌ Failed parsing {pdf_path}: {e}")

print("\nALL DONE ✅")
```

---

### 🔸 4️⃣ How to run

```bash
# 1. Install deps
pip install -r requirements.txt

# 2. Set Groq API key
export GROQ_API_KEY=your-groq-api-key

# 3. Put PDFs in /data

# 4. Run
python langchain_pipeline.py
```

---

### 🌟 Result:

```json
{
    "document_type": "Visa - Tourism",
    "visa_details": [
        {
            "issue_date": "...",
            "place_of_issue": "...",
            ...
        }
    ]
}
```

---

### 💡 Recap:

✅ Use **LangChain + Groq**
✅ Load PDF
✅ Classify document
✅ Extract structured fields (schema)
✅ Validate with Pydantic
✅ Save JSON
✅ Fully automatic!
