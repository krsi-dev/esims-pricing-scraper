import re
import bs4
import json
from .helpers import requests_soup
from .helpers import export_to_csv

STORE = 'redteago'
FILENAME = "redteago.csv"

def export():
    rows = []
    maps = None

    while not maps:
        page = requests_soup("https://redteago.com/")
        for script in page.select("script"):
            content = script.string or []
            if "iMapsData" in content:
                maps =  json.loads(content.replace("var iMapsData = ", "").replace(';', ''))

    for dat in maps["data"]:
        regions = dat["regions"]

        for r in regions:

            content = bs4.BeautifulSoup(r["tooltipContent"], features="html5lib").text.split('\n')
            packages = [x for x in content if "$" in x]

            for pack in packages:
                store       =   STORE
                price       =  "$" + pack.split("$")[-1]
                limit       =  pack.split('/')[0]
                validity    =  pack.split('/')[1].split("$")[0]
                network     =  'None'
                location    =  re.sub(r'\W+', ' ', r["name"])
                row = [store, price, validity, limit, network, location]
                row = [x.strip() for x in row]

                if row not in rows:
                    print(row)
                    rows.append(row)


                    export_to_csv(FILENAME, rows)
    return rows