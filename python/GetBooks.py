import requests
import pandas as pd

url = "https://demo.molecule.io/api/v2/books"


headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-email": "YOUR_EMAIL_HERE",
    "x-token": "YOUR_TOKEN_HERE"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    payload = response.json()
    records = payload.get("data", [])

    rows = []
    for item in records:
        attrs = item.get("attributes", {})
        custom = attrs.get("custom_field_values", {})

        rows.append({
            "id": item.get("id"),
            "type": item.get("type"),
            "name": attrs.get("name"),
            "created_at": attrs.get("created_at"),
            "updated_at": attrs.get("updated_at"),
            "updated_by": attrs.get("updated_by"),
            "origin": custom.get("Origin", "")
        })

    df = pd.DataFrame(rows)

    print("\nTABLE:\n")
    print(df.to_string(index=False))

    print("\nCOPY/PASTE INTO EXCEL:\n")
    print(df.to_csv(sep="\t", index=False))

    df.to_csv("books_export.csv", index=False)
    df.to_excel("books_export.xlsx", index=False)

    print("\nExported successfully:")
    print("books_export.csv")
    print("books_export.xlsx")

except requests.exceptions.HTTPError as e:
    print("HTTP error:", e)
    print("Response text:", response.text)
except Exception as e:
    print("Error:", e)
