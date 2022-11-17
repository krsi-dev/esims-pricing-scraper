import json
from .helpers import requests_soup
from .helpers import export_to_csv

STORE = 'travelsim'
FILENAME = "travelsim.csv"

def export():
    rows = []

    page = requests_soup("https://travelsim.com/configure-your-esim/")

    bundles = None
    countries = None

    for script in page.select("script"):
        content = script.string or []
        if "window.initialState" in content:
            bundles =  json.loads(content.replace("window.initialState = ", ""))
        
        if "window.listOfCountries" in content:
            countries = content.split("window.listOfCountries = ")[1].split('}]')[0] + '}]'
            countries = json.loads(countries)

    for item_key in bundles["bundledItems"].keys():
        bundle = bundles["bundledItems"][item_key]
        zone = bundle["zone"]
        
        locations = [x for x in countries if zone in x["zones"]]
        
        
        for location in locations:
            location_value = location["value"]

            for variation in bundle["variations"]:
                package = bundles["variations"][str(variation)]
                store       = STORE

                price = str(package["price"])
                price = price[:len(price)-2]
                price       = "$" + price

                validity    = package["validity_text"].split('for')[-1]
                limit       = package["name"]
                network     = "."
                location = location_value
                row = [store, price, validity, limit, network, location]
                row = [str(x).strip() for x in row]
                
                if row not in rows:
                    rows.append(row)
                    print(row)
                    export_to_csv(FILENAME, rows)

    return rows