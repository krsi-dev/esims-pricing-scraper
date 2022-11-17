from .helpers import requests_json
from .helpers import export_to_csv

STORE = 'airhubapp'
FILENAME = "airhubapp.csv"

def export():
    rows = []
    api_countries = requests_json(f"https://www.airhubapp.com/Home/BindDropdownCountry_web_v2?flag=3")

    for api_country in api_countries:
        try:
            api_traveller = requests_json(f"https://admin.airhubapp.com/JsonData/Traveller/{api_country['CountryName']}.json")
            api_plans = api_traveller["Plans"] or []

            for plan in api_plans:
                store       = STORE
                price       = "$" + str(plan["SellingCost"])
                validity    = plan["Vaildity"]
                limit       = f"{plan['DataAllowance']} {plan['DataAllowanceType']}".replace('null', '').replace('Select', '')
                network     = '.'
                location    = api_country["CountryName"]

                row = [store, price, validity, limit, network, location]
                row = [str(x).strip() for x in row]
                
                if row not in rows:
                    rows.append(row)
                    print(row)
                    export_to_csv(FILENAME, rows)
        except Exception:
            continue
    

    return rows