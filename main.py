from datetime import datetime, timedelta
from rates_data_manage import get_rates_data
import matplotlib.pyplot as plt

start_date = datetime(2025, 9, 25)
end_date = datetime.today() - timedelta(1)
currency = "BTCEUR"

data = get_rates_data(currency, start_date, end_date)
print("Nombre de cours d'echanges BTC en EURO :", len(data))


# Afficher graph
dates = [datetime.strptime(d["date"], "%Y/%m/%d") for d in data]
data_values = [float(d["value"]) for d in data]
plt.plot(dates, data_values)
plt.ylabel(currency)
plt.show()
