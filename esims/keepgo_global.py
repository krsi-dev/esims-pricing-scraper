from .helpers import requests_json
from .helpers import export_to_csv

STORE = 'keepgo_global'
FILENAME = "keepgo_global.csv"

def export():
    rows = []

    api = requests_json("https://myaccount.keepgo.com/api/v1/get_refills_by_shopify_id/319578523")

    for d in api:
        store       = STORE
        price       = f"${d['price_usd']}"
        validity    = "Unlimited"
        limit       = d["title"]
        network     = "."
        location    = "Global"

        row = [store, price, validity, limit, network, location]
        row = [str(x).strip() for x in row]
        
        if row not in rows:
            rows.append(row)
            print(row)
            export_to_csv(FILENAME, rows)
    return rows