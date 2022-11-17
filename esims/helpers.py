import os
import csv
import bs4
import requests
import fake_headers

def headers():
    headers = fake_headers.Headers(headers=True).generate()
    return headers

def requests_json(url):
    response = requests.get(url, headers=headers())
    return response.json()

def requests_soup(url):
    response = requests.get(url, headers=headers())
    soup = bs4.BeautifulSoup(response.content, features="html5lib")

    if soup.select_one(".wp-defender"):
        raise BaseException("Blocked by WP")
    return soup

def export_to_csv(filename, rows):
    cache_dir = 'cache'
    filepath = os.path.join(cache_dir, filename)

    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
    
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        headers = ["store", "price", "validity", "limit", "network", "location"]
        writer = csv.writer(f, delimiter=",")
        writer.writerow(headers)
        writer.writerows(rows)