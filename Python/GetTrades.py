import requests
import pandas as pd
import json

url = "https://demo.molecule.io/api/v2/trades?"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-email": "YOUR_EMAIL_HERE",
    "x-token": "YOUR_TOKEN_HERE"
}

#params = {
#    "quantity_type": "contract",
#    "product": "NG",
#    "price": 3.50,
#    "quantity": 20,
#    "tenor_start": "2026-12-01",
#    "tenor_end": "2026-12-31",
#    "fcm": "",
#    "notes": "Trade booked via TradeBlotter",
#    "tags": ["#demo"]
#}


response = requests.get(url, headers=headers)
response.raise_for_status()

data = response.json()

# Debug: see what the API actually returned
print("Top-level response type:", type(data).__name__)
if isinstance(data, dict):
    print("Top-level keys:", list(data.keys()))

# Extract the actual list of trade records
if isinstance(data, list):
    records = data
elif isinstance(data, dict):
    # Common API patterns
    if "data" in data and isinstance(data["data"], list):
        records = data["data"]
    elif "trades" in data and isinstance(data["trades"], list):
        records = data["trades"]
    else:
        raise ValueError(
            f"Could not find a list of records in the response. "
            f"Top-level keys: {list(data.keys())}"
        )
else:
    raise ValueError(f"Unexpected response type: {type(data).__name__}")

# Flatten nested JSON into columns
df = pd.json_normalize(records)

# Print the full table
print(df.to_string(index=False))

# Export files
csv_file = "trades_export.csv"
xlsx_file = "trades_export.xlsx"
json_file = "trades_export.json"

df.to_csv(csv_file, index=False)
df.to_excel(xlsx_file, index=False)
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

print(f"\nExported to:")
print(f" - {csv_file}")
print(f" - {xlsx_file}")
print(f" - {json_file}")
