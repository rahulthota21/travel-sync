import os
import openai
import requests
from dotenv import load_dotenv
from amadeus_token import get_amadeus_token

load_dotenv()

# Groq API – now using secure env variable
client = openai.Client(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def get_iata_code(city_name):
    try:
        prompt = f"Provide only the 3-letter IATA code for {city_name}, without any additional text or explanation."
        response = client.chat.completions.create(
            model="mistral-saba-24b",
            messages=[{"role": "user", "content": prompt}]
        )
        code = response.choices[0].message.content.strip().upper()
        return code if len(code) == 3 else None
    except Exception as e:
        print("IATA fetch error:", e)
        return None

def get_flight_offers(origin_city, destination_city, departure_date, budget="Luxury", adults=1):
    if budget.lower() != "luxury":
        return [{
            "mode": "Bus/Train",
            "suggestion": f"For {budget.lower()} budget, consider booking a train or bus between {origin_city} and {destination_city}. Use platforms like IRCTC, RedBus, or MakeMyTrip."
        }]

    origin_code = get_iata_code(origin_city)
    destination_code = get_iata_code(destination_city)

    if not origin_code or not destination_code:
        print("❌ Invalid IATA codes.")
        return []

    access_token = get_amadeus_token()
    if not access_token:
        return [{"mode": "error", "suggestion": "Unable to fetch flight access token."}]

    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    params = {
        "originLocationCode": origin_code,
        "destinationLocationCode": destination_code,
        "departureDate": departure_date,
        "adults": str(adults),
        "nonStop": "false",
        "max": "3"
    }

    headers = {
        'Authorization': f"Bearer {access_token}",
        'accept': "application/vnd.amadeus+json"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("data", [])
        else:
            print("✈️ Flight API error:", response.text)
            return []
    except Exception as e:
        print("✈️ Exception in flight fetch:", e)
        return []
