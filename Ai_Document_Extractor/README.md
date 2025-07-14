# 🧠 AI Document Schema Extractor

A production-grade Python pipeline to extract structured data from employee-related PDF documents using OCR and LLMs. The system takes a **document URL**, performs **OCR**, and extracts **schema-aligned JSON** using **LangChain** + **LLMs** or **prompt-engineered extraction**.

 > ✅ Already integrated with Odoo ERP for real-world employee document automation.
---

## 🚀 Project Overview

This project automates information extraction from various employee-related documents (e.g., passports, visas, employment contracts, change status, residence permits, healthcare certifications). It processes document URLs and returns structured data in JSON format using two robust pipelines:

* ✅ **OCR + LLM (via LangChain) with Pydantic schema validation**
* ✅ **OCR + Prompt-based schema extraction using LLM**

---

Great! Here’s the updated **README** with a new section highlighting the **Odoo integration**, plus a mention in the overview and future improvements.

---

# 🧠 AI Document Schema Extractor

A production-grade Python pipeline to extract structured data from employee-related PDF documents using OCR and LLMs. The system takes a **document URL**, performs **OCR**, and extracts **schema-aligned JSON** using **LangChain** + **LLMs** or **prompt-engineered extraction**.

✅ **Already integrated with [Odoo ERP](https://www.odoo.com/)** for real-world employee document automation.

---

## 🚀 Project Overview

This project automates information extraction from various employee-related documents (e.g., passports, visas, employment contracts, change status, residence permits, healthcare certifications). It processes document URLs (uploaded via Odoo) and returns structured data in JSON format using two robust pipelines:

* ✅ **OCR + LLM (via LangChain) with Pydantic schema validation**
* ✅ **OCR + Prompt-based schema extraction using LLM**

---

## 🔗 Odoo Integration

This project is **fully integrated with Odoo** and works directly with document uploads from the Odoo backend. Documents are uploaded and stored in the system, and their **URLs are passed to the extractor** for:

* Automated document processing
* Field extraction for employee onboarding
* JSON output compatible with Odoo modules
* Easy API-level integration for HR, admin, and payroll operations

> ✅ **Ready to plug into your Odoo HR or Document Management workflow**

---

## 📄 Document Flow

```mermaid
flowchart TD
    A[Uploaded Document URL] --> B[Download PDF]
    B --> C[Convert PDF to Image]
    C --> D[OCR using Qwen2-VL-2B-OCR]
    D --> E[Extracted Text]

    E --> F1[LangChain with Pydantic Schema]
    E --> F2[Prompt-based Schema in LLM]

    F1 --> G[Validated JSON Output]
    F2 --> G[Validated JSON Output]
    G --> H[Return JSON]
    H --> I[Stored Return JSON into Odoo Database]
```

---

## 🧰 Technologies Used

| Component             | Tool/Library                                              |
| --------------------- | --------------------------------------------------------- |
| **OCR**               | [Qwen2-VL-2B-OCR](https://huggingface.co/Qwen/Qwen-VL-2B) |
| **LLM Providers**     | OpenAI, DeepSeek, Ollama, Groq, etc.                      |
| **LLM Framework**     | [LangChain](https://www.langchain.com/)                   |
| **Schema Validation** | [Pydantic](https://docs.pydantic.dev/)                    |
| **PDF Handling**      | PyMuPDF (`fitz`), PIL                                     |
| **HTTP Client**       | `requests`                                                |

---

## 📦 Project Structure

```
Ai_Document_Extractor/
├── ai_data_detector/
│   ├── __init__.py
│   ├── config.py
│   ├── load_model.py
│   ├── read_pdf.py
│   ├── schema_extractor.py  # Using LangChain with Pydantic Schema and LLM
│   ├── schema_output.py
│   ├── schemas.py
├── setup.py
├── pyproject.toml         # (optional)
├── README.md              # (recommended)
├── requirements.txt       # (optional but helpful)
└── .gitignore             # (optional)

```

---

## ✅ Supported Document Types

| Document Type             | Extracted Fields                                                            |
| ------------------------- | --------------------------------------------------------------------------- |
| Passport                  | Passport number, name, DOB, issue/expiry date, profession                   |
| Visa (Tourism/Employment) | UID number, name, DOB, nationality, passport, profession, issue/valid dates |
| Change Status             | UID number, name, passport, employer, nationality, stamping deadline        |
| Employment Contract       | Contract duration, nationality, passport, DOB, academic qualification       |
| Residence                 | ID number, name, passport, profession, issue/expiry date                    |
| Healthcare Certificate    | DHA Unique ID, Professional name                                            |

---

## 🔧 How It Works

### 1. **Input**

A URL pointing to a PDF document uploaded in the backend (e.g., Odoo, ERP, HR system).

### 2. **Processing**

* The PDF is fetched and converted to images.
* Images are passed through `Qwen2-VL-2B-OCR` to extract raw text.
* OCR output is then passed to one of the following:

#### Approach 1: LangChain + Pydantic Schema

* LangChain prompts the LLM and parses the output into a validated schema using `Pydantic`.

#### Approach 2: Prompt-Based Schema

* The entire schema logic is embedded in the prompt.
* LLM returns structured JSON as response.

---

## 🧪 Example Output

```json
{
  "document_type": "Passport",
  "passport_details": [
    {
      "passport_number": "123456789",
      "name": "John Doe",
      "date_of_birth": "01/01/1990",
      "date_of_issue": "01/01/2020",
      "date_of_expiry": "01/01/2030",
      "profession": "Engineer"
    }
  ]
}
```

---

## 🛠️ Usage

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the extractor

```bash
python ai_data_detector/schema_output.py
```

Or via CLI:

```bash
ai-extract
```

### Example

```python
from schema_output import extract_document_schema_from_url

url = "http://example.com/path/to/document.pdf"
employee_id = "12345"
json_output = extract_document_schema_from_url(url, employee_id)
print(json_output)
```

---

## 🔐 API Key Configuration

- Set your LLM API key in the `.env` file or use the `get_api_key()` from `config.py`.
- Supports OpenAI, DeepSeek, Groq, Ollama, etc.


---

## 👨‍💻 Author

* **Mohammed Khalaf**
  >* Embedded & AI Developer

[GitHub](https://github.com/Mohammedkh97) | [LinkedIn](https://www.linkedin.com/in/mohammed-khalaf97/)--onelien