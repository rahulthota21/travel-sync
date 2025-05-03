import os
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.Client(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def get_travel_essentials(destination, start_date, season=None):
    prompt = f"""
    Generate a travel essentials checklist for a trip to {destination} starting on {start_date}.
    Include:
    - Weather-appropriate clothing
    - Electronics
    - Toiletries
    - Important documents
    - Local travel tips
    - Safety advice
    - Any local customs

    Return as a bullet list.
    """

    try:
        response = client.chat.completions.create(
            model="mistral-saba-24b",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ Error getting essentials:", e)
        return "Essentials could not be generated."
