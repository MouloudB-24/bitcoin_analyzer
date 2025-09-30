import json
from pathlib import Path
from typing import List

from api_service import binance_api_get_echanges_rate_extended
from datetime import datetime, timedelta

def load_json_data_from_file(filename):
    with open(filename, "r") as f:
        return json.load(f)


def extract_essential_data(row_data: List) -> List:
    data = []
    for d in row_data:
        date_obj = datetime.fromtimestamp(d[0] / 1000)
        data.append({"date": date_obj.strftime("%Y/%m/%d"), "value": d[4]})
    return data
     

def save_data_to_json(filename, data): 
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
        
def get_rates_data(currency, start_date, end_date):
    filename = currency + ".json"
    data = []
    
    if Path(filename).exists():
        print("Le fichier json existe")
        data = load_json_data_from_file(filename)
        
    if data:
        saved_start_date = datetime.strptime(data[0]["date"], "%Y/%m/%d")
        saved_end_date = datetime.strptime(data[-1]["date"], "%Y/%m/%d")
        
        if start_date < saved_start_date:
            print("Appel à l'API pour ajouter les données à gauche...")
            new_end_date = saved_start_date
            new_row_data = binance_api_get_echanges_rate_extended(currency, start_date, new_end_date)
            new_data = extract_essential_data(new_row_data)
            data = new_data + data

        if end_date > saved_end_date:
            print("Appel à l'API pour ajouter les données à droite...")
            new_start_date = saved_end_date + timedelta(1)
            new_row_data = binance_api_get_echanges_rate_extended(currency, new_start_date, end_date)
            new_data = extract_essential_data(new_row_data)
            data = data + new_data
        
        save_data_to_json(filename, data)
        
    else:
        print("Le fichier json n'existe pas")
        row_data = binance_api_get_echanges_rate_extended(currency, start_date, end_date)
        data = extract_essential_data(row_data)
        save_data_to_json(filename, data)
    
    return data



        

