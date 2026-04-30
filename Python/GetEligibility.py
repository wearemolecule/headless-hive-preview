import requests
import pandas as pd
import json
from pathlib import Path

url = "https://demo.molecule.io/api/v2/inventory/eligibility_rules"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-email": "YOUR_EMAIL_HERE",
    "x-token": "YOUR_TOKEN_HERE"
}

try:
    downloads_dir = Path.home() / "Downloads"
    downloads_dir.mkdir(parents=True, exist_ok=True)

    response = requests.get(url, headers=headers, timeout=30)

    print(f"Status: {response.status_code}")
    print(f"Request URL: {response.url}")

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

    # ---- File paths ----
    downloads_dir = Path.home() / "Downloads"
    excel_path = downloads_dir / "eligibility_rules_export.xlsx"
    csv_path = downloads_dir / "eligibility_rules_export.csv"
    json_path = downloads_dir / "eligibility_rules_export.json"

    # ---- Save files ----
    df.to_excel(excel_path, index=False)
    df.to_csv(csv_path, index=False)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    # ---- Output ----
    print("\nTABLE PREVIEW:\n")
    if df.empty:
        print("No records returned.")
    else:
        print(df.head().to_string(index=False))

    print(f"\nSaved Excel to: {excel_path}")
    print(f"Saved CSV to:   {csv_path}")
    print(f"Saved JSON to:  {json_path}")

except requests.exceptions.HTTPError as e:
    print("HTTP error:", e)
    print("Response text:", response.text)
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
except ValueError:
    print("Response was not valid JSON.")
    print(response.text)
except Exception as e:
    print("Unexpected error:", e)
