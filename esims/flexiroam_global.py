from .helpers import requests_soup
from .helpers import export_to_csv

STORE = 'flexiroam_global'
FILENAME = "flexiroam_global.csv"

def export():
    rows = []
    urls = [
        "https://travel.flexiroam.com/shop/?product-tags=global-prepaid-mobile-data",
        "https://travel.flexiroam.com/shop/page/2/?product-tags=global-prepaid-mobile-data"
    ]

    for url in urls:
        products = None

        while not products:
            page = requests_soup(url)
            products = [x for x in page.select(".post_data a") if "cart" not in x["href"] ]


        for product in products:
            page = None
            countries = None
            while not countries:
                page = requests_soup(product["href"])
                countries = page.select_one("div[data-tab='2'][role='tabpanel']")

            countries = countries.text.split(',')



            for country in countries:
                title = page.select_one("title").text.split('-')[0].split('+')
                store       = STORE
                price       = page.select_one(".woocommerce-Price-amount.amount").text
                validity    = [x for x in title[1].split(" ") if x][-2] + " Days"
                limit       = [x for x in title[1].split(" ") if x and "MB" in x or "GB" in x][0]
                network     = '.'
                location    = country

                row = [store, price, validity, limit, network, location]
                row = [str(x).strip() for x in row]
                
                if row not in rows:
                    rows.append(row)
                    print(row)
                    export_to_csv(FILENAME, rows)
    return rows