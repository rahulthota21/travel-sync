import os
import json
from datetime import datetime
from dotenv import load_dotenv

from itinerary_generator import extract_itinerary
from flight_search import get_flight_offers
from hotel_search import get_best_hotels_per_day
from amadeus_token import get_amadeus_token
from travel_essentials import get_travel_essentials

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def generate_trip_plan(user_prompt):
    print("\n📦 Extracting itinerary...")
    itinerary = extract_itinerary(user_prompt)
    if not itinerary:
        return

    origin = itinerary["origin_city"]
    destination = itinerary["destination_city"]
    start_date = itinerary["start_date"]
    trips = itinerary.get("trips", [])

    # Validate budget
    valid_budgets = ["Luxury", "Mid-range", "Economy"]
    budget = itinerary.get("budget", "Luxury")
    if budget not in valid_budgets:
        print("⚠️ Invalid budget returned:", budget)
        budget = "Luxury"

    print("\n✈️ Fetching flights...")
    flights = get_flight_offers(origin, destination, start_date, budget)

    print("\n🏨 Fetching hotel recommendations...")
    token = get_amadeus_token()
    hotels_per_day = get_best_hotels_per_day(trips, token)

    print("\n📋 Getting travel essentials...")
    essentials = get_travel_essentials(destination, start_date)

    full_plan = {
        "origin": origin,
        "destination": destination,
        "start_date": start_date,
        "budget": budget,
        "flights": flights,
        "hotels": hotels_per_day,
        "itinerary": trips,
        "essentials": essentials
    }

    filename = f"trip_plan_{destination}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(full_plan, f, indent=2)
    print(f"\n✅ Trip plan saved to {filename}")
