from .helpers import requests_soup
from .helpers import export_to_csv

STORE = 'flexiroam_regional'
FILENAME = "flexiroam_regional.csv"

def export():
    rows = []
    pages = None


    while not pages:
        page = requests_soup("https://travel.flexiroam.com/shop/?product-tags=regional-prepaid-mobile-data")
        pages = page.select("li > a.page-numbers")
        if pages:
            pages = max([int(page["href"].split("page/")[1].split("/")[0]) for page in pages])

    for page in range(1, pages):
        products = None
        
        while not products:
            url = f"https://travel.flexiroam.com/shop/page/{page}/?product-tags=single-country-prepaid-mobile-data"
            if page == 1:
                url = "https://travel.flexiroam.com/shop/?product-tags=regional-prepaid-mobile-data"
            page = requests_soup(url)
            products = page.select(".post_data")


        for product in products:
            title = product.select_one("h2 > a").text.split("+")
            store       = STORE
            price       = product.select_one(".woocommerce-Price-amount.amount").text
            validity    = [x for x in title[0].split(" ") if x][-2] + " Days"
            limit       = [x for x in title[0].split(" ") if x and "MB" in x or "GB" in x][0]
            network     = '.'
            location    = title[0].split(limit)[0]

            row = [store, price, validity, limit, network, location]
            row = [str(x).strip() for x in row]
            
            if row not in rows:
                rows.append(row)
                print(row)

                export_to_csv(FILENAME, rows)
    return rows