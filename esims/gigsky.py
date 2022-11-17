import requests
from .helpers import export_to_csv
from hurry.filesize import size

STORE = 'gigsky'
FILENAME = "gigsky.csv"


def export():
    rows = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'authorization': 'wixcode-pub.ef226effabd3920c2fbcfc142f040f22641aba9b.eyJpbnN0YW5jZUlkIjoiZWNkNmZlYTItN2YxZS00ZDkwLWJiNDktNzc5Y2Y4NjJkMjg3IiwiaHRtbFNpdGVJZCI6IjQwNWMyNjQ2LTYxOTQtNGNmZi1hMTk1LWU5MmZkMTRkY2EwMSIsInVpZCI6bnVsbCwicGVybWlzc2lvbnMiOm51bGwsImlzVGVtcGxhdGUiOmZhbHNlLCJzaWduRGF0ZSI6MTY2Nzk0NDI5ODAxNiwiYWlkIjoiZGQ4MjJkMzUtMWI4MS00MTgwLTk3NDAtNzlkN2Y0NDQyY2ZjIiwiYXBwRGVmSWQiOiJDbG91ZFNpdGVFeHRlbnNpb24iLCJpc0FkbWluIjpmYWxzZSwibWV0YVNpdGVJZCI6ImYyYmJhMGNhLWUxNWYtNDNhMS1iYWRjLWIzYmIzMWEwMGM0NCIsImNhY2hlIjpudWxsLCJleHBpcmF0aW9uRGF0ZSI6bnVsbCwicHJlbWl1bUFzc2V0cyI6IlNob3dXaXhXaGlsZUxvYWRpbmcsSGFzRG9tYWluLEFkc0ZyZWUiLCJ0ZW5hbnQiOm51bGwsInNpdGVPd25lcklkIjoiNThjMGMzMDUtYmU2My00NDM5LWEzMTktNWNkYWEzN2EzYTI1IiwiaW5zdGFuY2VUeXBlIjoicHViIiwic2l0ZU1lbWJlcklkIjpudWxsLCJwZXJtaXNzaW9uU2NvcGUiOm51bGx9',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.gigsky.com/_partials/wix-thunderbolt/dist/clientWorker.ca7066a6.bundle.min.js',
        'commonConfig': '%7B%22brand%22%3A%22wix%22%2C%22BSI%22%3A%22%22%7D',
        'x-wix-brand': 'wix',
        'X-Wix-Client-Artifact-Id': 'wix-thunderbolt',
    }

    json_data = {
        'collectionName': 'ConsumerPlans',
        'dataQuery': {
            'filter': {},
            'paging': {
                'offset': 0,
                'limit': 1000,
            },
        },
        'options': {},
        'includeReferencedItems': [],
        'segment': 'LIVE',
        'appId': '0eb18c68-aaad-48d9-bbe5-8f703aa0bafa',
    }

    response = requests.post('https://www.gigsky.com/_api/cloud-data/v1/wix-data/collections/query', headers=headers, json=json_data)
    items = response.json()["items"]

    plans = items[1]["json_response"]
    networks = items[2]["json_response"]["list"]

    for plan in plans:
        plan = plans[plan]
        items = plan["list"]
        
        for item in items:
            networkGroupId = item["networkGroupId"]
            network_ = [x for x in networks if x["networkGroupId"] == networkGroupId][0]

            store       = STORE
            price       = f"${item['price']}"
            validity    = str(int(item["validityPeriodInDays"])) + " Days"
            limit       = size(item["dataLimitInKB"] * 1024)
            limit += "B"
            network     = network_["imsiProvider"]
            location    = network_["networkGroupName"]

            row = [store, price, validity, limit, network, location]
            row = [str(x).strip() for x in row]
            
            if row not in rows:
                rows.append(row)
                print(row)

                export_to_csv(FILENAME, rows)
    return rows
