import requests
from .helpers import export_to_csv

STORE = 'esimplus'
FILENAME = "esimplus.csv"

def export():
    rows = []
    headers = {
        'authority': 'api.esimplus.net',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/json',
        'origin': 'https://esimplus.me',
        'referer': 'https://esimplus.me/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'x-firebase': ''
    }

    response = requests.get("https://api.esimplus.net/api/v6/plans", headers=headers)
    
    api = response.json()
    api_countries = api.get("data").get("countries")

    for api_country in api_countries:
        response = requests.get(f"https://api.esimplus.net/api/v6/country/{api_country['id']}", headers=headers)
        api_bundles = response.json()["data"]["bundles"]

        for api_bundle in api_bundles:
            bundles = api_bundle["bundles"]
            
            for key in bundles.keys():
                bundle = bundles[key]

                store       = STORE
                price       = f"${bundle['price']}"
                validity    = f"{bundle['days']} Days"
                limit       = f"{(int(key) * 0.001):.2f} GB"
                network     = api_bundle["operator"]
                location    = api_bundle["name"]

                row = [store, price, validity, limit, network, location]
                row = [str(x).strip() for x in row]
                
                if row not in rows:
                    rows.append(row)
                    print(row)

    
                    export_to_csv(FILENAME, rows)

    return rows