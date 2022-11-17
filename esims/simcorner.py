from .helpers import requests_soup
from .helpers import export_to_csv

STORE = 'simcorner'
FILENAME = "simcorner.csv"

def export():
    rows = []

    page_regions = None

    while not page_regions:
        page = requests_soup("https://simcorner.com/pages/regions")
        page_regions = page.select(".page_regions_main li > a[href*='sim-card']:not([class])")

    for region in page_regions:
        href = region["href"]
        items = None

        while not items:
            soup = requests_soup("https://simcorner.com" + href)
            items = soup.select(".carousel-cell")


        for item in items:
            store       = STORE
            price       = item.select_one(".sale-price").text
            validity    = item.select(".more_deails_inner > div")[-1:][0].select_one("div").text.split()[0] + " Days"
            limit       = item.select_one(".more_deails_inner > div:nth-child(3) > div").text.split("service")[0].split()[0]
            network     = "."
            location = soup.select_one("h1").text.split("Sim Cards")[0].replace("Buy", "")
            row = [store, price, validity, limit, network, location]
            row = [str(x).strip() for x in row]
            
            if row not in rows:
                rows.append(row)
                print(row)
                export_to_csv(FILENAME, rows)

        
        subcollection = soup.select("nav > ul > li > a[href*='sim-card']:not([class])")

        for sub in subcollection:
            items = None

            while not items:
                soup = requests_soup("https://simcorner.com" + sub["href"])
                items = soup.select(".carousel-cell")


            for item in items:
                store       = STORE
                price       = item.select_one(".sale-price").text
                validity    = item.select(".more_deails_inner > div")[-1:][0].select_one("div").text.split()[0] + " Days"
                limit       = item.select_one(".more_deails_inner > div:nth-child(3) > div").text.split("service")[0].split()[0]
                network     = "."
                location = soup.select_one("h1").text.replace("Buy Travel SIM Cards for", "").split("in")[0]
                row = [store, price, validity, limit, network, location]
                row = [str(x).strip() for x in row]
                
                if row not in rows:
                    rows.append(row)
                    print(row)
                    export_to_csv(FILENAME, rows)
    return rows