import requests
from .helpers import export_to_csv

STORE = 'breathesim'
FILENAME = "breathesim.csv"

def export():
    rows = []
    response = requests.get("https://manx.mobiliseconnect.com:7460/plans", headers={
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.6',
        'Connection': 'keep-alive',
        'Origin': 'https://www.breathesim.com',
        'Referer': 'https://www.breathesim.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'apikey': 'CfUg-rVBr3E_7k8x3-dMj_Gx6XpdF9',
        'companycode': 'Web',
    })
    
    api = response.json()
    api_packages = api.get("plans") or []

    for package in api_packages:
        store       = STORE
        price       = package["prices"][0]["currencySymbol"] + str(package["prices"][0]["cost"])
        validity    = str(package["validity"]) + " Days"
        limit       = f"{package['dataAllowance']} GB"
        network     = "."
        location    = package["planName"]

        row = [store, price, validity, limit, network, location]
        row = [str(x).strip() for x in row]
        
        if row not in rows:
            rows.append(row)
            print(row)

    
            export_to_csv(FILENAME, rows)
    return rows