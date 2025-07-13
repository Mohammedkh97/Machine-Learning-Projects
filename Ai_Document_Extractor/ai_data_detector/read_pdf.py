# file: read_pdf.py

import os
import requests
import fitz  # PyMuPDF
import io
from PIL import Image


def download_pdf(url, filename="file.pdf", save_to_disk=False):
    """
    Downloads a PDF from the given URL.

    Args:
        url (str): The URL to download the PDF from.
        filename (str): The filename to save the PDF as (if saving is enabled).
        save_to_disk (bool): Whether to save the PDF to disk.

    Returns:
        BytesIO: In-memory PDF file, or None if download fails.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        pdf_bytes = io.BytesIO(response.content)

        if save_to_disk:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"PDF saved: {filename}")
        else:
            print(f"PDF downloaded (in-memory): {filename}")

        return pdf_bytes

    except requests.exceptions.RequestException as e:
        print(f"Error downloading PDF: {e}")
        return None


def download_and_convert_pdf_to_image(
    url: str,
    filename: str = "file.pdf",
    save_to_disk: bool = False,
    save_image: bool = True,
    show_image: bool = False,
    dpi: int = 300,
):
    """
    Downloads a PDF from a URL and converts the first page to an image.

    Args:
        url (str): The URL to download the PDF from.
        filename (str): Local filename to save the PDF as (if saving).
        save_to_disk (bool): Save PDF to disk.
        save_image (bool): Save the converted image to file.
        show_image (bool): Show the image (works in Jupyter).
        dpi (int): Dots-per-inch resolution for the image.

    Returns:
        PIL.Image.Image: The image of the first page.
    """
    try:
        pdf_bytes = download_pdf(url, filename, save_to_disk)
        if not pdf_bytes:
            return None

        if save_to_disk:
            pdf_doc = fitz.open(filename)
        else:
            pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        if len(pdf_doc) == 0:
            raise ValueError("The PDF document is empty.")

        page = pdf_doc[0]
        pix = page.get_pixmap(dpi=dpi)  # type: ignore
        img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")

        if save_image:
            img.save("page_1.png")
            print("Saved image: page_1.png")

        if show_image:
            try:
                from IPython.display import display

                display(img)
            except ImportError:
                print("IPython not available. Use image.show() instead.")

        return img

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None


def extract_text_from_pdf(filename: str) -> str:
    """
    Extracts text from a local PDF file.

    Args:
        filename (str): Path to the PDF.

    Returns:
        str: All extracted text.
    """
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return ""

    try:
        doc = fitz.open(filename)
        text = "\n".join(page.get_text() for page in doc)  # type: ignore
        doc.close()
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""


# === Entry Point ===

if __name__ == "__main__":
    url = "https://americanamc-ammc-develop-21331446.dev.odoo.com/web/content/13542"
    filename = "sample.pdf"

    image = download_and_convert_pdf_to_image(
        url, filename, save_to_disk=False, show_image=False
    )

    if image:
        image.show()
    else:
        print("No image to display.")

    # Optional: Extract text from saved PDF
    # extracted_text = extract_text_from_pdf(filename)
    # print("Extracted Text:\n", extracted_text)
