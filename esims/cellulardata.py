from .helpers import requests_soup
from .helpers import export_to_csv

STORE = 'cellulardata'
FILENAME = "cellulardata.csv"

def export():
    rows = []

    plans = None
    
    while not plans:
        soup = requests_soup("https://cellulardata.ubigi.com/data-plans-and-coverage/ubigi-esim-data-plans/?destination=&currency=usd&one-off=on&monthly=on&annual=on")
        plans = soup.select(".plan.row")

    for plan in plans:
        store       = STORE
        price       = plan.select_one('.price').text.split('/')[0]
        validity    = plan.select_one('.validity').text.split('\n')[2].replace('-', '.')
        limit       = plan.select_one('.allowance').text
        network     = '.'
        location    = plan.select_one('.destination').text

        row = [store, price, validity, limit, network, location]
        row = [str(x).strip() for x in row]
        
        if row not in rows:
            rows.append(row)
            print(row)
    
            export_to_csv(FILENAME, rows)

    return rows