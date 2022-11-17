from .helpers import requests_soup
from .helpers import export_to_csv

STORE = 'simsdirect'
FILENAME = "simsdirect.csv"

def export():
    rows = []

    elements = None
    
    while not elements:
        soup = requests_soup("https://simsdirect.com.au/collections/all")
        elements = soup.select(".ProductItem")


    for el in elements:
        meta = el.select_one(".ProductItem__Title").text.strip()
        store       = STORE
        price       = el.select_one('.Price').text.split(' ')[-1:][0]
        validity    = meta.split('|')[-1:][0]
        limit       = meta.split('|')[-2:][0]
        network     = '.'
        location    = meta.split('Travel')[0]

        row = [store, price, validity, limit, network, location]
        row = [str(x).strip() for x in row]
        
        if row not in rows:
            rows.append(row)
            print(row)
    
            export_to_csv(FILENAME, rows)

    return rows