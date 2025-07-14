from setuptools import setup, find_packages

setup(
    name="ai-data-detector",
    version="0.1.0",
    description="Document Data Extractor using OCR, LLMs, and LangChain",
    author="Mohammed Khalaf",
    author_email="mohamedkhalaf201720200@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "openai",
        "langchain",
        "PyMuPDF",
        "pydantic",
        "transformers",
        "Pillow",
        "tqdm",
        "python-dotenv",
        "requests",
        "beautifulsoup4",
        "pdfminer.six",
        "scikit-learn",
        "numpy",
        "pandas",
    ],
    entry_points={
        "console_scripts": ["ai-extract=ai_data_detector.schema_output:main"],
    },
    python_requires=">=3.8",
)
# This setup script is used to package the ai-data-detector project.
# It specifies the project metadata, dependencies, and Python version requirements.
# Make sure to update the author_email with your actual email address.
# To install the package, run: pip install .
# To build the package, run: python setup.py sdist bdist_wheel
# To upload to PyPI, use: twine upload dist/*
# Ensure you have twine installed: pip install twine
# For development, you can use: pip install -e .
