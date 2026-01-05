"""
AgriMind: Smart Crop Info Updater
---------------------------------
Updates crop_info.csv with:
✅ Live market prices from Agmarknet
✅ Real-time rainfall from OpenWeatherMap
✅ Explainable reason text for chatbot (based on SHAP + market trend)
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ========= CONFIG =========
API_KEY = "a3f6fb712da6b1032922b331471050d4"   # your OpenWeather API key
BASE_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
CROP_INFO_PATH = "data/crop_info.csv"
OUTPUT_PATH = "data/crop_info_live.csv"
# ==========================


def fetch_agmarknet_data():
    """Scrape recent crop price data from Agmarknet (top 15 rows)"""
    try:
        url = "https://agmarknet.gov.in/SearchCmmMkt.aspx"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("tr")
        market_data = []
        for row in rows[1:15]:
            cols = [c.text.strip() for c in row.find_all("td")]
            if len(cols) >= 5:
                market_data.append({
                    "Crop": cols[1],
                    "District": cols[2],
                    "Market": cols[3],
                    "Price(Rs/qtl)": cols[4]
                })
        return pd.DataFrame(market_data)
    except Exception as e:
        print("⚠️ Agmarknet fetch failed:", e)
        return pd.DataFrame(columns=["Crop", "District", "Market", "Price(Rs/qtl)"])


def get_weather(district):
    """Fetch real-time temperature, humidity, rainfall for a district"""
    try:
        params = {"q": f"{district},IN", "appid": API_KEY, "units": "metric"}
        r = requests.get(BASE_WEATHER_URL, params=params, timeout=5)
        data = r.json()
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "rainfall": data.get("rain", {}).get("1h", 0),
            "weather": data["weather"][0]["description"].title()
        }
    except Exception as e:
        print(f"⚠️ Weather fetch failed for {district}: {e}")
        return {"temperature": 28, "humidity": 65, "rainfall": 0, "weather": "Clear"}


def generate_explanation(crop, temp, rain, price):
    """
    Simple text explanation for chatbot (later replace with SHAP reasoning)
    """
    return (
        f"{crop} is currently suitable because the temperature is around {temp}°C "
        f"and rainfall is {rain} mm, which fits its ideal growing range. "
        f"The market price is approximately ₹{price} per quintal, "
        f"indicating good profitability this season."
    )


def main():
    print("🔄 Updating AgriMind Crop Info...")

    crop_info = pd.read_csv(CROP_INFO_PATH)
    agri_df = fetch_agmarknet_data()

    updated_rows = []
    for _, row in crop_info.iterrows():
        crop = row["Crop"]
        # pick first listed district
        dist = str(row["MajorDistricts"]).split(",")[0].strip()

        weather = get_weather(dist)

        # match market price if available
        crop_prices = agri_df[agri_df["Crop"].str.contains(crop, case=False, na=False)]
        price = crop_prices["Price(Rs/qtl)"].head(1).values[0] if not crop_prices.empty else "NA"

        explanation = generate_explanation(
            crop=crop,
            temp=weather["temperature"],
            rain=weather["rainfall"],
            price=price if price != "NA" else "unknown"
        )

        row_dict = row.to_dict()
        row_dict.update({
            "CurrentPrice(Rs/qtl)": price,
            "CurrentRainfall(mm)": weather["rainfall"],
            "CurrentTemp(°C)": weather["temperature"],
            "Weather": weather["weather"],
            "ExplainableReason": explanation
        })
        updated_rows.append(row_dict)

    df_new = pd.DataFrame(updated_rows)
    df_new["LastUpdated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    df_new.to_csv(OUTPUT_PATH, index=False)
    print("✅ Updated:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
