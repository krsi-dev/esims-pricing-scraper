import re
from .helpers import requests_soup
from .helpers import export_to_csv

STORE = 'airsim'
FILENAME = "airsim.csv"

def export():
    rows = []
    site_urls = ["https://www.airsim.com.sg/all_regions?limit=100", "https://www.airsim.com.sg/all_regions?limit=100&page=2"]
    
    for site_url in site_urls:
        soup = None
        product_urls = None

        while not product_urls:
            soup = requests_soup(site_url)
            product_urls = [x["href"] for x in soup.select("a[href*='?path=62&limit=100']")]

        product_urls = list(set(product_urls))

        for product_url in product_urls:
            elements = None

            while not elements:
                soup = requests_soup(product_url)
                elements = soup.select("div.radio.bt-image-option")

                for el in elements:
                    el_text = el.text
                    
                    if "Days" in el_text:
                        timeline = "Days"
                    elif "Day" in el_text:
                        timeline = "Day"
                    elif "hrs" in el_text:
                        timeline = "hrs"
                    elif "Hours" in el_text:
                        timeline = "Hours"


                    store       = STORE
                    price       = "SG$ " + el_text.split("SG$")[-1:][0]
                    validity    = re.split(r'(^[^\d]+)', el_text.split("SG$")[0])[-1:][0].split(timeline)[0] + f" {timeline}"
                    limit       = re.split(r'(^[^\d]+)', el_text.split("SG$")[0])[-1:][0].split(timeline)[1]
                    network     = re.split(r'(^[^\d]+)', el_text.split("SG$")[0])[1:][0]
                    location    = soup.title.text.split('-')[0]

                    if "GB" in limit:
                        limit = limit.split("G")[0].split()[0] + "GB"
                    else:
                        limit = "Unlimited"

                    if network.strip() == location.strip():
                        network = "n/a"

                    row = [store, price, validity, limit, network, location]
                    row = [str(x).strip() for x in row]
                    
                    if row not in rows:
                        rows.append(row)
                        print(row)
    
                        export_to_csv(FILENAME, rows)
    return rows