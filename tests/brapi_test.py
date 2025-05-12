import requests
import os
from dotenv import load_dotenv
from rich import print

load_dotenv()

BRAPI_TOKEN = os.getenv("BRAPI_TOKEN")

response = requests.get(f"https://brapi.dev/api/quote/list?token={BRAPI_TOKEN}")

data = response.json()

tickers_data = data.get('stocks')

print(tickers_data)