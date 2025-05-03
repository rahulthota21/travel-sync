import os
import requests
from dotenv import load_dotenv

load_dotenv()  # ✅ Load variables from .env

def get_amadeus_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': os.getenv('AMADEUS_CLIENT_ID'),
        'client_secret': os.getenv('AMADEUS_CLIENT_SECRET')
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("❌ Failed to retrieve Amadeus token:", response.text)
        return None
