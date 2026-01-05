# src/ingestion/market_ingestion.py
import os, requests, pandas as pd
from datetime import date, timedelta

OGD_BASE = "https://api.data.gov.in/resource/{rid}"

def fetch_mandi_prices(commodity: str, state: str = None, district: str = None,
                       market: str = None, days: int = 30) -> pd.DataFrame:
    api_key = os.getenv("DATA_GOV_API_KEY")
    rid = os.getenv("AGMARKNET_RESOURCE_ID")
    assert api_key and rid, "Set DATA_GOV_API_KEY and AGMARKNET_RESOURCE_ID in .env"
    end = date.today()
    start = end - timedelta(days=days+3)  # small cushion
    params = {
        "api-key": api_key,
        "format": "json",
        "limit": 10000,
        "filters[commodity]": commodity,
        "filters[arrival_date_from]": start.strftime("%d/%m/%Y"),
        "filters[arrival_date_to]": end.strftime("%d/%m/%Y"),
    }
    if state: params["filters[state]"] = state
    if district: params["filters[district]"] = district
    if market: params["filters[market]"] = market
    url = OGD_BASE.format(rid=rid)
    r = requests.get(url, params=params, timeout=25)
    r.raise_for_status()
    recs = r.json().get("records", [])
    if not recs: return pd.DataFrame()
    df = pd.DataFrame(recs)
    # normalize numeric
    for c in ["modal_price","min_price","max_price"]:
        if c in df: df[c] = pd.to_numeric(df[c], errors="coerce")
    if "arrival_date" in df:
        df["arrival_date"] = pd.to_datetime(df["arrival_date"], dayfirst=True, errors="coerce")
        df = df.sort_values("arrival_date")
    return df

def engineer_market_features(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"price_latest": None, "price_med30": None, "price_trend7": None, "price_z30": None}
    last = float(df["modal_price"].iloc[-1])
    med30 = float(df["modal_price"].tail(30).median())
    # simple trend: last 7 vs prior 7 median
    s7 = df["modal_price"].tail(7).mean()
    p7 = df["modal_price"].tail(14).head(7).mean() if len(df) >= 14 else df["modal_price"].mean()
    trend7 = float((s7 - p7) / max(p7, 1e-6))
    # z-score vs 30d
    s30 = df["modal_price"].tail(30)
    z30 = float((last - s30.mean()) / (s30.std(ddof=1) if s30.std(ddof=1) > 0 else 1.0))
    return {"price_latest": last, "price_med30": med30, "price_trend7": trend7, "price_z30": z30}
