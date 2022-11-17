from .helpers import requests_json
from .helpers import export_to_csv

STORE = 'ifreemogos'
FILENAME = "ifreemogos.csv"

def export():
    rows = []
    api = requests_json("https://apiv2.ifreegroup.cn/v4/esim/packages-web?_t=1667827324062")
    api_packages = api.get("data") or []

    for package in api_packages:
        packages = package["packages"]

        for package_ in packages:
            group_id = package_["group_id"]
            product_id = package_["product_id"]

            data = requests_json(f"https://apiv2.ifreegroup.cn/v4/esim/package/details?_t=1667827371795&group_id={group_id}&product_id={product_id}")["data"]
            package_list = data["package_list"]
            countries = data["countries"]

            for country in countries:
                for item in package_list:           

                    limit_num = round(item['capacity'] / 1024)

                    if limit_num:
                        limit_num = f"{limit_num} GB"
                    else:
                        limit_num = f"{item['capacity']} MB"

                    store       = STORE
                    price       = f"${item['price']}"
                    validity    = f"{item['day']} Days"
                    limit       = limit_num
                    network     = country["provider_title"]
                    location    = country["country_name"]

                    row = [store, price, validity, limit, network, location]
                    row = [str(x).strip() for x in row]
                    
                    if row not in rows:
                        rows.append(row)
                        print(row)
    
                        export_to_csv(FILENAME, rows)

    return rows