# 🌍 TravelSync — AI-Powered Trip Planner

> Create personalized travel plans using AI, flight data, hotel search, photo recognition, and local recommendations — all in one Streamlit app.

---

## ✨ Features

- 🧠 **AI-Powered Itinerary Generator** using Groq/OpenAI
- ✈️ **Live Flight Search** powered by Amadeus API
- 🏨 **Hotel Recommendations** with Geolocation filtering
- 📸 **Photo-Based Destination Recognition** using Google Vision & Places
- 🧳 **Travel Essentials Checklist** based on location & season
- 💬 **Natural Language & Structured Input Support**
- ⚙️ Built using `Streamlit`, `OpenAI`, `Groq`, `Google APIs`, and `Amadeus`

---

## 🚀 Demo Usage

Upload a photo or enter a prompt like:

> *Plan a 4-day trip from Delhi to Manali starting June 10 with a mid-range budget.*

You’ll get:
- ✈️ Flights  
- 🗓️ Itinerary  
- 🏨 Hotels  
- 🧳 Essentials Checklist  

---

## 🛠️ Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/travel-sync.git
cd travel-sync
```

### 2. Create a Virtual Environment (Optional)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add API Keys

Create a `.env` file based on `.env.example`:

```env
AMADEUS_CLIENT_ID=your-amadeus-client-id
AMADEUS_CLIENT_SECRET=your-amadeus-client-secret
GROQ_API_KEY=your-groq-api-key
GOOGLE_API_KEY=your-google-api-key
```

### 5. Run the App
```bash
streamlit run app.py
```

---

## 🔐 APIs Used

| API                   | Provider       | Purpose                         |
|------------------------|----------------|----------------------------------|
| OpenAI / Groq          | LLM Generator  | Generate itinerary & recognition |
| Amadeus Travel API     | Amadeus        | Flights and hotel data           |
| Google Maps & Vision   | Google Cloud   | Geocoding, image analysis, POIs  |

---

## 📂 Project Structure

```
.
├── app.py                  # Streamlit app entry
├── ver/                   # Modular business logic
│   ├── amadeus_token.py
│   ├── flight_search.py
│   ├── hotel_search.py
│   ├── itinerary_generator.py
│   ├── place_recognizer.py
│   ├── travel_essentials.py
│   └── trip_pipeline.py
├── .env.example            # Sample environment variables
├── requirements.txt        # Python dependencies
├── .gitignore              # Git exclusions
```

---

## 🙌 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Groq](https://groq.com/)
- [Amadeus Travel APIs](https://developers.amadeus.com/)
- [Google Cloud Vision](https://cloud.google.com/vision)
- [OpenAI](https://openai.com/)

## 👨‍💻 Contributors

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/rahulthota21">
        <img src="https://avatars.githubusercontent.com/rahulthota21" width="100px;" alt="rahulthota21"/>
        <br /><sub><b>Thota Rahul</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Kowshik4593">
        <img src="https://avatars.githubusercontent.com/Kowshik4593" width="100px;" alt="Kowshik4593"/>
        <br /><sub><b>Kowshik Padala</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/99sarath">
        <img src="https://avatars.githubusercontent.com/99sarath" width="100px;" alt="99sarath"/>
        <br /><sub><b>Sarath Chandra</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/teja-actions">
        <img src="https://avatars.githubusercontent.com/teja-actions" width="100px;" alt="teja-actions"/>
        <br /><sub><b>Peruri Teja Sai Sathwik</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/chdvv15">
        <img src="https://avatars.githubusercontent.com/chdvv15" width="100px;" alt="chdvv15"/>
        <br /><sub><b>Chappidi Dinesh</b></sub>
      </a>
    </td>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/u/0000000?v=4" width="100px;" alt="Unknown Contributor"/>
      <br /><sub><b>Chethan Kalyan</b></sub>
    </td>
  </tr>
</table>
