from .helpers import requests_soup
from .helpers import export_to_csv

STORE = 'zimconnections'
FILENAME = "zimconnections.csv"

def export():
    rows = []
    page = requests_soup("https://www.zimconnections.com/zim-plans")

    for card in page.select("div[data-tab='global'] div.c-plans-card"):
        store       = STORE
        price       = card.select_one(".c-plans-card__price").text
        validity    = card.select_one(".c-plans-card__duration").text
        limit       = card.select_one(".c-plans-card__duration").text
        network     = "."
        location    = "Global"

        row = [store, price, validity, limit, network, location]
        row = [str(x).strip() for x in row]
        
        if row not in rows:
            rows.append(row)
            print(row)
            export_to_csv(FILENAME, rows)

    for card in page.select("div[data-tab='europe-regional'] div.c-plans-card"):
        store       = STORE
        price       = card.select_one(".c-plans-card__price").text
        validity    = card.select_one(".c-plans-card__duration").text
        limit       = card.select_one(".c-plans-card__duration").text
        network     = "."
        location    = "Europe"

        row = [store, price, validity, limit, network, location]
        row = [str(x).strip() for x in row]
        
        if row not in rows:
            rows.append(row)
            print(row)
            export_to_csv(FILENAME, rows)

    for card in page.select("div[data-tab='usa-regional'] div.c-plans-card"):
        store       = STORE
        price       = card.select_one(".c-plans-card__price").text
        validity    = card.select_one(".c-plans-card__duration").text
        limit       = card.select_one(".c-plans-card__duration").text
        network     = "."
        location    = "USA"

        row = [store, price, validity, limit, network, location]
        row = [str(x).strip() for x in row]
        
        if row not in rows:
            rows.append(row)
            print(row)
            export_to_csv(FILENAME, rows)

    for card in page.select("div[data-tab='asia-pacific-regional'] div.c-plans-card"):
        store       = STORE
        price       = card.select_one(".c-plans-card__price").text
        validity    = card.select_one(".c-plans-card__duration").text
        limit       = card.select_one(".c-plans-card__duration").text
        network     = "."
        location    = "Asia Pacific"

        row = [store, price, validity, limit, network, location]
        row = [str(x).strip() for x in row]
        
        if row not in rows:
            rows.append(row)
            print(row)
            export_to_csv(FILENAME, rows)
    return rows