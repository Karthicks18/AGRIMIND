{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3088167a-7e03-4012-b867-68a7fe6a73b9",
   "metadata": {},
   "outputs": [],
   "source": [
    "import json\n",
    "import joblib\n",
    "from datetime import datetime, timedelta\n",
    "from src.weather_api import get_7day_forecast_by_latlon\n",
    "from src.market_api import get_market_price_mandi\n",
    "from src.scoring import compute_expected_profit\n",
    "\n",
    "CROP_MODEL_PATH = \"AgriMind/models/crop_model.pkl\"\n",
    "CROP_METADATA_PATH = \"AgriMind/data/crop_metadata.json\"\n",
    "\n",
    "# Load model & metadata once\n",
    "model = joblib.load(CROP_MODEL_PATH)\n",
    "with open(CROP_METADATA_PATH, \"r\") as f:\n",
    "    crop_meta = json.load(f)\n",
    "\n",
    "def generate_crop_plan(lat, lon, soilN, soilP, soilK, selected_date=None):\n",
    "    if not selected_date:\n",
    "        selected_date = datetime.today().strftime(\"%Y-%m-%d\")\n",
    "\n",
    "    # --- Weather & Market inputs ---\n",
    "    wf = get_7day_forecast_by_latlon(lat, lon)\n",
    "    results = []\n",
    "\n",
    "    for crop_name, meta in crop_meta.items():\n",
    "        price_info = get_market_price_mandi(crop_name)\n",
    "        feat = [soilN, soilP, soilK, wf[\"avg_temp_7d\"], wf[\"sum_rain_7d\"], price_info[\"price_7day_avg\"]]\n",
    "        pred_score = model.predict_proba([feat])[0] if hasattr(model, \"predict_proba\") else [1.0]\n",
    "        score = float(max(pred_score))\n",
    "        expected_yield = 20 + (score * 10)  # simulated yield (quintals/ha)\n",
    "        fert_cost = 2000\n",
    "        profit_data = compute_expected_profit(crop_name, expected_yield, price_info[\"price_now\"], fert_cost)\n",
    "\n",
    "        plan = {\n",
    "            \"crop\": crop_name.title(),\n",
    "            \"duration_days\": meta[\"duration_days\"],\n",
    "            \"expected_yield\": expected_yield,\n",
    "            \"expected_profit\": profit_data[\"profit\"],\n",
    "            \"market_trend_pct\": price_info[\"trend_pct\"],\n",
    "            \"recommended_fertilizers\": meta[\"recommended_fertilizers\"],\n",
    "            \"harvest_date\": (datetime.strptime(selected_date, \"%Y-%m-%d\") + timedelta(days=meta[\"duration_days\"])).strftime(\"%Y-%m-%d\")\n",
    "        }\n",
    "        results.append(plan)\n",
    "\n",
    "    # Sort by profit\n",
    "    results = sorted(results, key=lambda x: x[\"expected_profit\"], reverse=True)\n",
    "    return results[0], results\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
