# src/recommender.py
import requests
import pandas as pd

def fetch_agmarknet_price(crop, state="TN"):
    """
    Try to fetch the latest modal price for `crop` from Agmarknet (state-level).
    Returns a numeric price (₹/kg) or None if unavailable.
    """
    try:
        # Agmarknet commodity/state URL - works with read_html for many commodities
        url = f"https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity={crop}&Tx_State={state}"
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return None

        tables = pd.read_html(res.text, flavor="bs4")
        # Find a table with a price-like column
        for df in tables:
            # Look for common price column keywords
            price_cols = [c for c in df.columns if any(k in c.lower() for k in ["modal", "price", "max", "min"])]
            if price_cols:
                col = price_cols[0]
                # Try convert last non-null value
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "").str.extract(r"([-+]?\d*\.?\d+)")[0], errors="coerce")
                df = df.dropna(subset=[col])
                if not df.empty:
                    latest = float(df[col].iloc[-1])
                    # If Agmarknet prices are per quintal or per 100kg in some tables, they often use kg. 
                    # We'll assume ₹/kg here; if values look very large (>500), the dataset may be per 100kg — keep as-is for now.
                    return latest
        return None
    except Exception:
        return None
