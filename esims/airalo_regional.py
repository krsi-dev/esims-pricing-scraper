from .helpers import requests_soup
from .helpers import requests_json
from .helpers import export_to_csv

STORE = 'airalo_regional'
FILENAME = "airalo_regional.csv"

def export():
    rows = []
    site = requests_soup("https://www.airalo.com/regional-esim")
    site_elements = site.select("div > div > a > div > p")

    for element in site_elements:
        element_region = "-".join(element.text.lower().split())
        api_package = requests_json(f"https://www.airalo.com/api/v2/regions/{element_region}")
        api_packages = api_package["packages"] or []

        for package in api_packages:
            store       = STORE
            price       = "$" + str(package["price"])
            validity    = package["validity"]
            limit       = package["data"]
            network     = package["operator"]["title"]
            location    = element_region

            row = [store, price, validity, limit, network, location]
            row = [str(x).strip() for x in row]
            
            if row not in rows:
                rows.append(row)
                print(row)


                export_to_csv(FILENAME, rows)

    return rows