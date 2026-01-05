# src/ingestion/weather_ingestion.py
import requests, pandas as pd

OPEN_METEO = "https://api.open-meteo.com/v1/forecast"

def fetch_weather(lat: float, lon: float, days: int = 7) -> pd.DataFrame:
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["precipitation_sum","temperature_2m_max","temperature_2m_min","relative_humidity_2m_mean"],
        "forecast_days": days,
        "timezone": "auto"
    }
    # Open-Meteo accepts daily as csv list
    params["daily"] = ",".join(params["daily"])
    r = requests.get(OPEN_METEO, params=params, timeout=20)
    r.raise_for_status()
    d = r.json()["daily"]
    return pd.DataFrame(d)

def engineer_weather_features(df: pd.DataFrame) -> dict:
    # Expect columns: time, precipitation_sum, temperature_2m_max, temperature_2m_min, relative_humidity_2m_mean
    rain_7d = float(pd.to_numeric(df["precipitation_sum"]).sum())
    rain_days = int((pd.to_numeric(df["precipitation_sum"]) >= 1.0).sum())
    tmax = float(pd.to_numeric(df["temperature_2m_max"]).mean())
    tmin = float(pd.to_numeric(df["temperature_2m_min"]).mean())
    rh = float(pd.to_numeric(df["relative_humidity_2m_mean"]).mean())
    # Map to crop-model features (temperature, humidity, rainfall)
    return {
        "temperature": (tmax + tmin) / 2.0,
        "humidity": rh,
        "rainfall": rain_7d,
        "rain_days": rain_days
    }
