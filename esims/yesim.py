from .helpers import requests_json
from .helpers import export_to_csv

STORE = 'yesim'
FILENAME = "yesim.csv"

def export():
    rows = []
    data = requests_json(" https://iweb.yesim.app/v1/countries_for_sale?lang=en")

    for dat in data[0]:
        plans = requests_json(f"https://iweb.yesim.app/v1/new_plans_for_sale?country={dat['country']}&lang=en")

        for plan in plans:
            mb = round(int(plan['totalMb']) / 1024)
            if mb == 0:
                mb = f"{plan['totalMb']} MB"
            else:
                mb = f"{mb} GB"
    
            store       = STORE
            location    = plan["planName"]
            price       = f"${plan['planCost']}"
            limit       = mb
            validity    = f"{plan['validityPeriod']} Days" 
            network     = "."
            row = [store, price, validity, limit, network, location]
            row = [x.strip() for x in row]

            if row not in rows:
                print(row)
                rows.append(row)
    
                export_to_csv(FILENAME, rows)

    return rows