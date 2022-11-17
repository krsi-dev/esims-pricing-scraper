from .helpers import requests_json
from .helpers import export_to_csv

STORE = 'simtex'
FILENAME = "simtex.csv"

def export():
    rows = []
    data = requests_json("https://api.simtexglobal.com/v1/countries?lang=en")

    for dat in data["countries"]:
        country_name = dat["name"]
        country_code = dat["code"]

        data = requests_json(f"https://api.simtexglobal.com/v1/packages?country={country_code}&lang=en")

        try:
            for dat in data["packages"]:
                store       = "simtex"
                location    = country_name
                price       = f"${dat['price']['usdPrice']}"

                meta = dat["name"].split('-')
                limit       = meta[0]
                validity    = meta[1].split()[0].replace("D", " Days")
                network     = "."
                row = [store, price, validity, limit, network, location]
                row = [x.strip() for x in row]

                if row not in rows:
                    print(row)
                    rows.append(row)
                    export_to_csv(FILENAME, rows)
        except Exception:
            continue


    
    
    return rows