from .helpers import requests_json
from .helpers import export_to_csv

STORE = 'soracommobile'
FILENAME = "soracommobile.csv"

def export():
    rows = []
    data = requests_json("https://api.soracommobile.com/public/data-plans?locale=en")

    for dat in data:
        countries = dat["countries"]
        plans = dat["plans"]

        for country in countries:
            country_name = country["name"]
            for plan in plans:
                store       = "soracommobile"

                location    = country_name
                price       = f"${plan['price']}"
                limit       = f"{plan['capacity'] / 1000} GB"
                validity    = f"{plan['period']} Days"
                network     = "."
                
                row = [store, price, validity, limit, network, location]
                row = [x.strip() for x in row]

                if row not in rows:
                    print(row)
                    rows.append(row)
                    export_to_csv(FILENAME, rows)
    

    return rows