from datetime import datetime, date, timedelta
import requests

from api_config import BASE_URL


def get_dates_intervals(start_date: datetime, end_date: datetime, max_days: int):
    diff_days = (end_date - start_date).days
    dates_interval = []
    interval_begin_date = start_date
    while diff_days > 0:
        nb_days_to_add = max_days - 1
        interval_ending_date = interval_begin_date + timedelta(nb_days_to_add)
        
        if diff_days <= max_days:
            interval_ending_date = end_date
   
        dates_interval.append([interval_begin_date, interval_ending_date])
        interval_begin_date = interval_ending_date + timedelta(1)
        diff_days -= max_days
    return dates_interval
        

def binance_api_get_echanges_rate(currency: str, start_date: datetime, end_date: datetime):
    url = BASE_URL + "api/v3/klines"
    params = {
        "symbol": currency,
        "interval": "1d",
        "startTime": int(start_date.timestamp() * 1000),
        "endTime": int(end_date.timestamp() * 1000)
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error during HTTP request: {response.status_code}")
        return None
    
    data = response.json()
    return data


def binance_api_get_echanges_rate_extended(currency, start_date: datetime, end_date: datetime):
    all_data = []
    dates_intervals = get_dates_intervals(start_date, end_date, 500)   
    if dates_intervals:
        for interval in dates_intervals:
            all_data += binance_api_get_echanges_rate(currency, interval[0], interval[1])
    return all_data
