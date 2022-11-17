from .helpers import requests_json
from .helpers import export_to_csv

STORE = 'numeroesim'
FILENAME = "numeroesim.csv"

def export():
    rows = []
    countries = requests_json("https://www.numeroesim.com/numero-external.php?variable=data_package_countries")

    for country in countries:
        packages = requests_json(f"https://www.numeroesim.com/numero-external.php?variable=data_packages_list&type=countries&country_id={country['id']}")["packages"]

        for package in packages:
            store       = STORE
            price       = "$" + str(package["price"])
            validity    = package["days"] + " Days"
            limit       =  package["quota"] + package["unit"]
            network     = package["additonal_info"].split("Operates on the (")[1].split(")")[0]
            location    = package["name"]

            row = [store, price, validity, limit, network, location]
            row = [str(x).strip() for x in row]
            
            if row not in rows:
                rows.append(row)
                print(row)



                export_to_csv(FILENAME, rows)
    return rows