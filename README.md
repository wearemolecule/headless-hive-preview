# headless-hive-preview



A reference implementation demonstrating how to query the [Molecule](https://www.molecule.io) REST API using Python. This repository provides working sample scripts and example output payloads for clients who want to integrate with Molecule's HIVE platform or build custom extensions on top of the Molecule API.

---

## Overview

HIVE is Molecule's front-end trading and risk platform. For clients who want to extend HIVE or build their own tooling, Molecule exposes a comprehensive REST API at `/api/v2`. This repo shows real request/response examples for the most common data domains:

- **Allocations** — position allocation records
- **Books** — trading book hierarchy
- **Valuations** — MTM and P&L data
- **Trades** — trade records and lifecycle
- **Counterparties** — counterparty master data
- **Eligibility** — product eligibility rules
- **Obligations** — settlement obligations
- **Tickets** — inventory tickets

Each script in the `Python/` directory is a self-contained example that authenticates, calls a single endpoint, and prints a sample of the response.

---

## Requirements

- Python 3.8+
- `requests` library (`pip install requests`)
- A Molecule API token and registered email address (contact your Molecule account manager to obtain credentials)

---

## Setup

1. Clone the repository:

```bash
git clone https://github.com/wearemolecule/headless-hive-preview.git
cd headless-hive-preview
```

2. Install dependencies:

```bash
pip install requests
```

3. Set your credentials as environment variables (recommended) or edit the config at the top of each script:

```bash
export MOLECULE_API_TOKEN="your-api-token"
export MOLECULE_API_EMAIL="your-email@example.com"
```

---

## Usage

All scripts follow the same pattern: authenticate via headers, call the relevant `/api/v2` endpoint, and print the JSON response.

```bash
python Python/get_allocations.py
python Python/get_books.py
python Python/get_valuations.py
python Python/get_trades.py
python Python/get_counterparties.py
python Python/get_eligibility.py
python Python/get_obligations.py
python Python/get_tickets.py
```

The `Molecule Sample Data.xlsx` file in the root of the repo contains representative sample output for each endpoint, useful for understanding the schema before writing your own integration.

---

## Configuration

| Variable | Description |
|---|---|
| `MOLECULE_API_TOKEN` | Your API token, generated in the Molecule UI under Settings → API |
| `MOLECULE_API_EMAIL` | The email address associated with your Molecule account |
| `MOLECULE_BASE_URL` | Base URL — US: `https://app.molecule.io/api/v2`, EU: `https://eu.molecule.io/api/v2` |

Every request requires two HTTP headers:

```python
headers = {
    "X-Token": MOLECULE_API_TOKEN,
    "X-Email": MOLECULE_API_EMAIL,
}
```

---

## Examples

### Get Allocations

```python
import requests

response = requests.get(
    "https://app.molecule.io/api/v2/allocations",
    headers={"X-Token": TOKEN, "X-Email": EMAIL},
)
print(response.json())
```

### Get Books

```python
response = requests.get(
    "https://app.molecule.io/api/v2/books",
    headers={"X-Token": TOKEN, "X-Email": EMAIL},
)
print(response.json())
```

### Get Valuations

```python
response = requests.get(
    "https://app.molecule.io/api/v2/valuations",
    params={"as_of": "2024-01-31"},
    headers={"X-Token": TOKEN, "X-Email": EMAIL},
)
print(response.json())
```

### Get Trades

```python
response = requests.get(
    "https://app.molecule.io/api/v2/trades",
    headers={"X-Token": TOKEN, "X-Email": EMAIL},
)
print(response.json())
```

### Get Counterparties

```python
response = requests.get(
    "https://app.molecule.io/api/v2/counterparties",
    headers={"X-Token": TOKEN, "X-Email": EMAIL},
)
print(response.json())
```

### Get Eligibility

```python
response = requests.get(
    "https://app.molecule.io/api/v2/eligibility",
    headers={"X-Token": TOKEN, "X-Email": EMAIL},
)
print(response.json())
```

### Get Obligations

```python
response = requests.get(
    "https://app.molecule.io/api/v2/obligations",
    headers={"X-Token": TOKEN, "X-Email": EMAIL},
)
print(response.json())
```

### Get Tickets

```python
response = requests.get(
    "https://app.molecule.io/api/v2/inventory/tickets",
    headers={"X-Token": TOKEN, "X-Email": EMAIL},
)
print(response.json())
```

---

### Pagination

List endpoints return paginated results (default page size: 1,000 records). Use `page` and `items` query parameters to paginate:

```python
# Fetch page 2 with 500 records per page
response = requests.get(
    "https://app.molecule.io/api/v2/trades",
    params={"page": 2, "items": 500},
    headers={"X-Token": TOKEN, "X-Email": EMAIL},
)

# Return all records in a single call
response = requests.get(
    "https://app.molecule.io/api/v2/trades",
    params={"items": "all"},
    headers={"X-Token": TOKEN, "X-Email": EMAIL},
)
```

---

## Further Documentation

Full API reference including all endpoints, parameters, and schemas is available in the Molecule OpenAPI specification. Contact your Molecule account team for access to `developer.molecule.io`.

---

## License

MIT — see [LICENSE](LICENSE) for details.