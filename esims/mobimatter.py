from .helpers import requests_soup
from .helpers import export_to_csv

STORE = 'mobimatter'
FILENAME = "mobimatter.csv"

def export():
    rows = []
    urls = [
        "https://mobimatter.com/travel-esim/asia",
        "https://mobimatter.com/travel-esim/middle-east",
        "https://mobimatter.com/travel-esim/oceania",
        "https://mobimatter.com/travel-esim/america",
        "https://mobimatter.com/travel-esim/europe",
        "https://mobimatter.com/travel-esim/africa"
    ]

    for url in urls:
        country = url.split('/')[-1:][0]
        soup = requests_soup(url)

        products = soup.select('body > div.chakra-container > div > div > div > div > div > div > div > div.css-0')
        
        
        for product in products:
            details = product.select(".css-1rtr3sq")
            store       = "mobimatter"
            price       = details[2].text.split(':')[-1:][0]
            validity    = details[0].text.split(':')[-1:][0]
            limit       = details[1].text.split(':')[-1:][0]
            network     = "."
            location    = country
            row = [store, price, validity, limit, network, location]
            row = [x.strip() for x in row]
            if row not in rows:
                print(row)
                rows.append(row)

    
                export_to_csv(FILENAME, rows)

    return rows