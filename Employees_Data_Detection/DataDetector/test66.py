import requests

def download_pdf(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"PDF downloaded successfully: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading PDF: {e}")
        
        

url = "https://www.example.com/sample.pdf"
filename = "sample.pdf"
download_pdf(url, filename)
