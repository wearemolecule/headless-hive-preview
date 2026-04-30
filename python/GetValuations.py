import requests
import pandas as pd
import json
from pathlib import Path

url = "https://demo.molecule.io/api/v2/valuations"

params = {
    "as_of": "2026-04-29",
   ## "book": "#AzaleaSprings",
   ## "trade_id": ,
  # "product": 'F.NYISO.ZONEB.HRLY',
   "include": "leg_id",
   "include": "extended"
}

headers = {
    "accept": "application/json",
    "x-email": "YOUR_EMAIL_HERE",
    "x-token": "YOUR_TOKEN_HERE"
}

downloads_dir = Path.home() / "Downloads"
downloads_dir.mkdir(parents=True, exist_ok=True)

response = requests.get(url, headers=headers, params=params)
response.raise_for_status()

payload = response.json()
records = payload.get("data", [])

# ---- Flatten into table ----
df = pd.json_normalize(records)

# Clean column names
df.columns = [col.replace("attributes.", "") for col in df.columns]

# Convert lists/dicts to strings for Excel
for col in df.columns:
    df[col] = df[col].apply(
        lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x
    )

# ---- File names ----
as_of = params.get("as_of", "unknown_date")
book = params.get("book", "all_books").replace("#", "")

excel_path = downloads_dir / f"valuations_{book}_{as_of}.xlsx"
json_path = downloads_dir / f"valuations_{book}_{as_of}.json"

# ---- Save files ----
df.to_excel(excel_path, index=False)

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2)

# ---- Output ----
print("\nTABLE:\n")
print(df.head().to_string(index=False))  # preview only

print(f"\nSaved Excel to: {excel_path}")
print(f"Saved JSON to:  {json_path}")
