# file: config.py
from dotenv import load_dotenv
import os


def get_api_key():
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API")
    # print(api_key)  # Should print your key (or part of it)
    return api_key
