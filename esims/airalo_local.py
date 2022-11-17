from .helpers import requests_json
from .helpers import export_to_csv

STORE = 'airalo_local'
FILENAME = "airalo_local.csv"

def export():
    rows = []
    api_countries = requests_json("https://www.airalo.com/api/v2/countries?sort=asc")

    for api_country in api_countries:
        api_package = requests_json(f"https://www.airalo.com/api/v2/countries/{api_country['slug']}")
        api_packages = api_package["packages"] or []

        for package in api_packages:
            store       = STORE
            price       = "$" + str(package["price"])
            validity    = package["validity"]
            limit       = package["data"]
            network     = package["operator"]["title"]
            location    = api_country['slug']

            row = [store, price, validity, limit, network, location]
            row = [str(x).strip() for x in row]
            
            if row not in rows:
                rows.append(row)
                print(row)

                export_to_csv(FILENAME, rows)
    
    return rows