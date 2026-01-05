{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "598293e8-9cb6-4ca0-9e4a-ad4845d9bf88",
   "metadata": {},
   "outputs": [],
   "source": [
    "import json\n",
    "\n",
    "CROP_METADATA_PATH = \"AgriMind/data/crop_metadata.json\"\n",
    "with open(CROP_METADATA_PATH, \"r\") as f:\n",
    "    crop_meta = json.load(f)\n",
    "\n",
    "def get_fertilizer_schedule(crop_name, crop_age_days):\n",
    "    crop_name = crop_name.lower()\n",
    "    if crop_name not in crop_meta:\n",
    "        return {\"error\": \"Crop not found\"}\n",
    "\n",
    "    ferts = crop_meta[crop_name][\"recommended_fertilizers\"]\n",
    "    duration = crop_meta[crop_name][\"duration_days\"]\n",
    "    stage = \"unknown\"\n",
    "\n",
    "    # Determine growth stage\n",
    "    total = 0\n",
    "    for stage_name, stage_days in crop_meta[crop_name][\"growth_stages\"].items():\n",
    "        total += stage_days\n",
    "        if crop_age_days <= total:\n",
    "            stage = stage_name\n",
    "            break\n",
    "\n",
    "    fert_reco = []\n",
    "    for fert_type, days_list in ferts.items():\n",
    "        for d in days_list:\n",
    "            if crop_age_days <= d:\n",
    "                fert_reco.append({\n",
    "                    \"fertilizer\": fert_type.title(),\n",
    "                    \"day_of_application\": d,\n",
    "                    \"stage\": stage\n",
    "                })\n",
    "    if not fert_reco:\n",
    "        return {\"message\": \"No further fertilizer needed — nearing maturity.\"}\n",
    "\n",
    "    return {\n",
    "        \"crop\": crop_name.title(),\n",
    "        \"crop_age_days\": crop_age_days,\n",
    "        \"stage\": stage,\n",
    "        \"next_fertilizer_schedule\": fert_reco\n",
    "    }\n"
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
