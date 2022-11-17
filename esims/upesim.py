import bs4
import requests
from .helpers import requests_soup
from .helpers import export_to_csv

STORE = 'upesim'
FILENAME = "upesim.csv"

def export():
    rows = []
    urls = [
        "https://www.upesim.com/en/esim-esim/",
        "https://www.upesim.com/en/esim-esim/?page=2",
        "https://www.upesim.com/en/esim-esim/?page=3",
        "https://www.upesim.com/en/esim-esim/?page=4"
    ]

    for url in urls:
        soup = requests_soup(url)
        products = soup.select("article.product-item")
        
        for product in products:
            id_product = product["data-id-product"]
            id_product_attribute = product["data-id-product-attribute"]
            headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.upesim.com',
            'Referer': 'https://www.upesim.com/en/esim-esim/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            }
            params = {
                'controller': 'product',
            }

            data = {
                'action': 'quickview',
                'id_product': id_product,
                'id_product_attribute': id_product_attribute,
            }

            response = requests.post('https://www.upesim.com/en/index.php', params=params, headers=headers, data=data)
            data = response.json()["product"]
            meta = data["meta_description"]
            meta_sp = meta.split('.')

            try:
                store       = STORE
                location    = meta_sp[0].split('with')[0].replace('eSIM', '')
                price       = meta_sp[1].split('for')[1] + "." + meta_sp[2].split()[0]
                limit       = meta_sp[1].split('for')[0].split('Internet')[0]
                validity    = bs4.BeautifulSoup(data["embedded_attributes"]["description_short"], features="html.parser").select_one("h3").text.replace("Validity", "").replace(".", "")
                network     = meta_sp[3].split('the')[1].replace(')', '')
                row = [store, price, validity, limit, network, location]
                row = [x.strip() for x in row]

                if row not in rows:
                    print(row)
                    rows.append(row)
                    export_to_csv(FILENAME, rows)
            except Exception:
                continue
    

    return rows