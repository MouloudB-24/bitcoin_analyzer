import json
from pathlib import Path
from typing import List

from api_service import binance_api_get_echanges_rate, binance_api_get_echanges_rate_extended, get_dates_intervals
from datetime import datetime, timedelta, date

number_of_days = 3

end_date = datetime.today()
start_date = datetime(2025, 9, 28)

asset = "BTCEUR"
filename = asset + ".json"


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
        



# data = []
# if Path(filename).exists():
#     data = load_json_data_from_file(filename)
    
# if data:
#     saved_start_date = datetime.strptime(data[0]["date"], "%Y/%m/%d")
#     saved_end_date = datetime.strptime(data[-1]["date"], "%Y/%m/%d")
    
#     apres = False
#     if start_date < saved_start_date:
#         end_date = saved_start_date
       
#     elif start_date > saved_end_date:
#         start_date = saved_end_date + timedelta(1)
#         apres = True
#     else:
#         start_date = saved_end_date + timedelta(1)
#         apres = True
        
#     row_data = binance_api_get_echanges_rate(asset, start_date, end_date)
#     new_data = extract_essential_data(data)
#     if apres:
#         data += new_data
#     else:
#         data = new_data + data 
#     save_data_to_json(filename, data)
    
# else:
#     row_data = binance_api_get_echanges_rate(asset, start_date, end_date)
#     data = extract_essential_data(row_data)
#     save_data_to_json(filename, data)


row_data = binance_api_get_echanges_rate_extended(datetime(2024, 1, 1), datetime(2024, 12, 31))

print(len(row_data))



    

