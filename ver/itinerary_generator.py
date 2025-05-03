import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()

client = openai.Client(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def extract_itinerary(prompt):
    groq_prompt = f"""
You are a travel assistant. Generate a detailed day-by-day travel itinerary based on the following prompt.

Return JSON with:
- origin_city
- destination_city
- start_date (YYYY-MM-DD)
- budget (must be one of: Luxury, Mid-range, Economy)
- trips: a list of entries with:
  - day (number)
  - date (YYYY-MM-DD)
  - city
  - activities: list of activities with:
      - time
      - title
      - description

User prompt: {prompt}
"""
    try:
        response = client.chat.completions.create(
            model="mistral-saba-24b",
            messages=[{"role": "user", "content": groq_prompt}]
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content[7:-3].strip()
        return json.loads(content)
    except Exception as e:
        print("❌ Error parsing Groq response:", e)
        return None
