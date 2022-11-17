from .helpers import requests_json
from .helpers import export_to_csv

STORE = 'airalo_global'
FILENAME = "airalo_global.csv"

def export():
    rows = []
    api = requests_json("https://www.airalo.com/api/v2/regions/world")
    api_packages = api.get("packages") or []

    for package in api_packages:
        package_countries = package["operator"]["countries"]

        for package_country in package_countries:
            store       = STORE
            price       = "$" + str(package["price"])
            validity    = package["validity"]
            limit       = package["data"]
            network     = package["operator"]["title"]
            location    = package_country["title"]

            row = [store, price, validity, limit, network, location]
            row = [str(x).strip() for x in row]
            
            if row not in rows:
                rows.append(row)
                print(row)
                export_to_csv(FILENAME, rows)

    return rows