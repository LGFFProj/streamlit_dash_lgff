import requests

def get_products():
    
    url = "https://api.exchange.coinbase.com/products"

    response = requests.get(url)

    ids = [item['id'] for item in response.json()]

    ids.sort()

    if response.status_code == 200:
        return ids
    else:
        response.raise_for_status()