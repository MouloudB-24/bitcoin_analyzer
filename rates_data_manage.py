import json
from pathlib import Path
from typing import List

from binance_api_service import binance_api_get_exchanges_filtred_rate_extended
from datetime import datetime, timedelta

def load_json_data_from_file(filename):
    with open(filename, "r") as f:
        return json.load(f)


def extract_essential_data(row_data: List) -> List:
    data = []
    for d in row_data:
        date_obj = datetime.fromtimestamp(d[0] / 1000)
        data.append({"date": date_obj.strftime("%Y/%m/%d"), "value": float(d[4])})
    return data
     

def save_data_to_json(filename, data): 
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
        
def get_and_manage_rates_data(currency, start_date, end_date):
    filename = currency + ".json"
    data = []
    exclud_nb_days_start = 0
    exclud_nb_days_end = 0
    if Path(filename).exists():
        print("Le fichier json existe")
        data = load_json_data_from_file(filename)

    if data:
        saved_start_date = datetime.strptime(data[0]["date"], "%Y/%m/%d")
        saved_end_date = datetime.strptime(data[-1]["date"], "%Y/%m/%d")
        nb_days_start = (saved_start_date - start_date).days
        if nb_days_start > 0:
            print("Appel à l'API pour ajouter les données à gauche...")
            new_end_date = saved_start_date
            new_row_data = binance_api_get_exchanges_filtred_rate_extended(currency, start_date, new_end_date)
            new_data = extract_essential_data(new_row_data)
            data = new_data + data
        elif nb_days_start < 0:
            exclud_nb_days_start = -nb_days_start
            
        nb_days_end =  (saved_end_date - (end_date - timedelta(1))).days
        if nb_days_end < 0:
            print("Appel à l'API pour ajouter les données à droite...")
            new_start_date = saved_end_date + timedelta(1)
            new_row_data = binance_api_get_exchanges_filtred_rate_extended(currency, new_start_date, end_date)
            new_data = extract_essential_data(new_row_data)
            data = data + new_data
        else:
            exclud_nb_days_end = nb_days_end
        
        save_data_to_json(filename, data)
        
    else:
        print("Le fichier json est vide")
        row_data = binance_api_get_exchanges_filtred_rate_extended(currency, start_date, end_date)
        data = extract_essential_data(row_data)
        save_data_to_json(filename, data)
        
    
    if exclud_nb_days_start > 0:
        data = data[exclud_nb_days_start:]
        
    if exclud_nb_days_end > 0:
        data = data[:-exclud_nb_days_end]
    return data



        

