from .helpers import requests_json
from .helpers import export_to_csv

STORE = 'knowroaming'
FILENAME = "knowroaming.csv"

def export():
    rows = []
    api = requests_json("https://esim-app.telna.com/api/countries?str=")

    for dat in api:
        dat = dat["region"]
        plans = dat["plans"]

        for plan in plans:
            store       = "knowroaming"
            price       = f"${plan['price']}"
            validity    = f"{plan['validity']} Days"
            limit       = plan["data"]
            network     = "."
            location    = dat["details"]["name"]

            row = [store, price, validity, limit, network, location]
            row = [str(x).strip() for x in row]
            
            if row not in rows:
                rows.append(row)
                print(row)
    
                export_to_csv(FILENAME, rows)

    return rows