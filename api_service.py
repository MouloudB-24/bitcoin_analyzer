# Tous les appels à l'API
from datetime import datetime
import requests
import json

from api_config import BASE_URL

def coindesk_api_get_echanges_rates():
    url = BASE_URL + "api/v3/klines"
    params = {
        "symbol": "BTCEUR",
        "interval": "1d",  # 1 jour
        "startTime": int(datetime(2021, 1, 1).timestamp() * 1000),
        "endTime": int(datetime(2021, 1, 11).timestamp() * 1000),
        "limit": 10
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error during HTPP request: {response.status_code}")
        return None
    else:
        json_response = response.json()
        price_close = []
        for r in json_response:
            timestamp = r[0] / 1000
            date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
            close_price = float(r[4])
            
            price_close.append((date, close_price))
        return price_close
    
