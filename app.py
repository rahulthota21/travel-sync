
import streamlit as st
from trip_pipeline import generate_trip_plan
from pathlib import Path
import json
from datetime import datetime, timedelta
from travel_essentials import get_travel_essentials
from place_recognizer import recognize_place_from_image

st.set_page_config(page_title="TravelSync", layout="wide")
st.title("🌍 TravelSync: AI-Powered Trip Planner")

if "trip_generated" not in st.session_state:
    st.session_state.trip_generated = False
if "photo_place" not in st.session_state:
    st.session_state.photo_place = None

tab1, tab2, tab3 = st.tabs(["✍️ Free Prompt", "📋 Structured Search", "📸 Photo Search"])

# Free Prompt Tab
with tab1:
    st.subheader("Describe your trip in natural language")
    free_prompt = st.text_input("Trip description", placeholder="e.g. Plan a 5-day trip to Goa from Hyderabad starting April 10")

    if st.button("Generate Itinerary (Free Prompt)"):
        with st.spinner("Generating trip..."):
            generate_trip_plan(free_prompt)
            st.session_state.trip_generated = True

# Structured Form
with tab2:
    st.subheader("Structured Trip Planner")

    default_dest = st.session_state.photo_place if st.session_state.photo_place else ""
    origin = st.text_input("From (City)", "")
    destination = st.text_input("To (City)", value=default_dest)
    start_date = st.date_input("Start Date", datetime.today() + timedelta(days=1))
    days = st.number_input("Number of Days", min_value=1, max_value=30, value=2 if default_dest else 5)
    budget = st.selectbox("Budget", ["Economy", "Mid-range", "Luxury"])
    preferences = st.multiselect("Preferences", ["Beach", "Food", "Nightlife", "Temples", "Trekking", "Nature"])
    constraints = st.text_area("Constraints (optional)", "")

    if st.button("Generate Itinerary (Structured)"):
        if not origin or not destination:
            st.warning("Please enter both source and destination cities.")
        else:
            prompt = f"Plan a {days}-day trip from {origin} to {destination} starting on {start_date.strftime('%B %d, %Y')} with a {budget} budget. Preferences: {', '.join(preferences) if preferences else 'none'}. Constraints: {constraints or 'none'}."
            with st.spinner("Generating trip..."):
                generate_trip_plan(prompt)
                st.session_state.trip_generated = True
                st.session_state.photo_place = None

# Image Recognition
with tab3:
    st.subheader("Upload a Place Photo to Start Planning")

    image = st.file_uploader("Upload an image (JPG, PNG)", type=["jpg", "jpeg", "png"])
    if image and st.button("Recognize & Plan"):
        img_path = f"temp_{datetime.now().timestamp()}.jpg"
        with open(img_path, "wb") as f:
            f.write(image.read())
        result = recognize_place_from_image(img_path)
        if result:
            st.success("Place Recognized!")
            st.image(result["photo_url"], use_column_width=True)
            st.markdown(f"**📍 {result['name']}**")
            st.markdown(f"📫 {result['address']}")
            st.markdown(f"⭐ {result['rating']} ({result['total_reviews']} reviews)")
            st.markdown(f"[🌐 View on Google Maps]({result['maps_link']})")

            st.session_state.photo_place = result['name']
            st.success("🎯 Head to 'Structured Search' tab to finish planning your trip.")
        else:
            st.error("Could not recognize the place.")

# Output
if st.session_state.trip_generated:
    latest_file = sorted(Path(".").glob("trip_plan_*.json"), key=lambda x: x.stat().st_mtime, reverse=True)[0]

    with open(latest_file, "r") as f:
        plan = json.load(f)

    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader(f"🧭 Trip: {plan['origin']} → {plan['destination']} (Start: {plan['start_date']})")

        if plan.get("flights"):
            st.subheader("✈️ Flights")
            if isinstance(plan["flights"][0], dict) and plan["flights"][0].get("mode") == "Bus/Train":
                st.warning("This budget does not support flights. Please use the Structured tab to customize transportation options.")
            else:
                for fdata in plan["flights"]:
                    for s in fdata["itineraries"][0]["segments"]:
                        dep = datetime.strptime(s["departure"]["at"], "%Y-%m-%dT%H:%M:%S")
                        arr = datetime.strptime(s["arrival"]["at"], "%Y-%m-%dT%H:%M:%S")
                        st.markdown(f"- **{s['carrierCode']} {s['number']}**: {s['departure']['iataCode']} → {s['arrival']['iataCode']} | {dep.strftime('%b %d, %I:%M %p')} → {arr.strftime('%I:%M %p')}")

        st.subheader("🗓️ Itinerary")
        hotel_map = {h["day"]: h["hotels"] for h in plan["hotels"]}
        for d in plan["itinerary"]:
            st.markdown(f"### Day {d['day']} – {d['date']} ({d['city']})")
            for act in d["activities"]:
                st.markdown(f"- **{act['time']}**: *{act['title']}* — {act['description']}")
            for h in hotel_map.get(d["day"], []):
                st.markdown(f"🏨 [{h['name']}]({h['booking_link']}) ([Map]({h['google_maps']}))")

    with col2:
        st.subheader("🧳 Essentials")
        essentials = get_travel_essentials(plan['destination'], plan['start_date'])
        st.markdown(essentials)
