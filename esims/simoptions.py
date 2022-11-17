from .helpers import requests_soup
from .helpers import export_to_csv

STORE = 'simoptions'
FILENAME = "simoptions.csv"

def export():
    rows = []
    site_offers = None

    while not site_offers:
        site = requests_soup("https://www.simoptions.com/esim-offers/")
        site_offers = site.select("a[href*='esim-'].btn.btn-white.d-block")

    for element in site_offers:
        element_href = element["href"]
        
        blocks = None
        while not blocks:
            soup = requests_soup(element_href)
            blocks = soup.select(".product-sale-block")
        
        for block in blocks:
            store       = STORE
            price       = block.select_one(".woocommerce-Price-amount.amount").text
            validity    = block.select_one("table.simcard-meta > tbody > tr:nth-child(4) > td").text
            limit       = block.select_one("table.simcard-meta > tbody > tr:nth-child(1) > td").text
            network     = block.select_one(".package-sub-title").text
            location    = soup.select_one(".landing-title").text.split()[0]

            row = [store, price, validity, limit, network, location]
            row = [str(x).strip() for x in row]
            
            if row not in rows:
                rows.append(row)
                print(row)

                export_to_csv(FILENAME, rows)

    return rows