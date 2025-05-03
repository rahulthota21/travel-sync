import requests
import urllib.parse


def get_coordinates(place, api_key):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": place, "key": api_key}
    res = requests.get(url, params=params).json()
    if res["status"] == "OK":
        return res["results"][0]["geometry"]["location"].values()
    return None, None

def get_hotels_by_geocode(lat, lon, token):
    url = f"https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-geocode"
    params = {"latitude": lat, "longitude": lon, "radius": 10}
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers, params=params)
    return res.json().get("data", []) if res.status_code == 200 else []

def get_best_hotels_per_day(itinerary, api_key, token):
    hotels_by_day = []
    for day in itinerary:
        activities = day.get("activities", [])
        if not activities: continue
        title = activities[-1]["title"]
        city = day["city"]
        location = f"{title} {city} Goa" if "Flight" not in title else f"{city} Goa"
        lat, lon = get_coordinates(location, api_key)
        if lat and lon:
            hotels = get_hotels_by_geocode(lat, lon, token)[:3]
            suggestions = []
            for h in hotels:
                name = h["name"]
                q = urllib.parse.quote_plus(f"{name} Goa")
                suggestions.append({
                    "name": name,
                    "google_maps": f"https://www.google.com/maps/search/?api=1&query={q}",
                    "booking_link": f"https://www.booking.com/searchresults.html?ss={q}"
                })
            hotels_by_day.append({
                "day": day["day"],
                "date": day["date"],
                "city": city,
                "hotels": suggestions
            })
    return hotels_by_day
