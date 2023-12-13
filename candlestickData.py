import requests

def get_data(product_id, granularity, start_time=None, end_time=None):
    
    base_url = "https://api.exchange.coinbase.com"
    endpoint = f"/products/{product_id}/candles"
    url = f"{base_url}{endpoint}"

    params = {
    "granularity": granularity,
    "start_time": start_time,
    "end_time": end_time,
    }

    params = {key: value for key, value in params.items() if value is not None}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response
    else:
        response.raise_for_status()