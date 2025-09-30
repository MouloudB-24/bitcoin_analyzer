from datetime import datetime
from rates_date_manage import get_rates_data
import matplotlib.pyplot as plt

start_date = datetime(2019, 1, 1)
end_date = datetime(2021, 5, 30) #datetime.today()
currency = "BTCEUR"

data = get_rates_data(currency, start_date, end_date)
print("Nombre de cours d'echanges BTC en EURO :", len(data))

dates = [datetime.strptime(d["date"], "%Y/%m/%d") for d in data]
data_values = [float(d["value"]) for d in data]
plt.plot(dates, data_values)
plt.ylabel(currency)
plt.show()