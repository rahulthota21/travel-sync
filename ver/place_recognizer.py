import os
import requests
import base64
import json
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def recognize_place_from_image(image_path):
    with open(image_path, "rb") as img_file:
        img_bytes = base64.b64encode(img_file.read()).decode("utf-8")

    vision_url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_API_KEY}"
    vision_payload = {
        "requests": [{
            "image": {"content": img_bytes},
            "features": [{"type": "LANDMARK_DETECTION", "maxResults": 1}]
        }]
    }
    vision_res = requests.post(vision_url, json=vision_payload)
    vision_json = vision_res.json()

    if "error" in vision_json:
        print("❌ Vision API error:", vision_json["error"])
        return None

    responses = vision_json.get("responses")
    if not responses or not isinstance(responses, list):
        print("❌ Invalid response from Vision API:", vision_json)
        return None

    landmark_annotation = responses[0].get("landmarkAnnotations", [])
    if not landmark_annotation:
        print("❌ No landmarks detected.")
        return None

    keyword = landmark_annotation[0]["description"]

    # Google Places API
    places_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": keyword, "key": GOOGLE_API_KEY}
    res = requests.get(places_url, params=params).json()

    if res["status"] != "OK":
        print("❌ Places API error:", res)
        return None

    place = res["results"][0]
    name = place["name"]
    address = place.get("formatted_address")
    rating = place.get("rating")
    reviews = place.get("user_ratings_total")

    photo_ref = place.get("photos", [{}])[0].get("photo_reference")
    photo_url = (
        f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=600&photoreference={photo_ref}&key={GOOGLE_API_KEY}"
        if photo_ref else None
    )

    return {
        "name": name,
        "address": address,
        "rating": rating,
        "total_reviews": reviews,
        "maps_link": f"https://www.google.com/maps/search/?api=1&query={name.replace(' ', '+')}",
        "photo_url": photo_url
    }
