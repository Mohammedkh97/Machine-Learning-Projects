import os
import requests
import fitz


def download_pdf(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"PDF downloaded successfully: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading PDF: {e}")


def extract_text_from_pdf(filename):
    try:
        doc = fitz.open(filename)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

# === Entry Point ===


if __name__ == "__main__":
    url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    filename = "sample.pdf"
    download_pdf(url, filename)
    extracted_text = extract_text_from_pdf(filename)

    print("Extracted Text:\n", extracted_text)
    
