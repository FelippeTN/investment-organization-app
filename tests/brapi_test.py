import requests
import os
from dotenv import load_dotenv

load_dotenv()

BRAPI_TOKEN = os.getenv("BRAPI_TOKEN")

response = requests.get(f"https://brapi.dev/api/quote/BBAS3.SA?token={BRAPI_TOKEN}")

print(response.text)