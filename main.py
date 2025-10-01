from datetime import datetime
from rates_data_manage import get_and_manage_rates_data
import matplotlib.pyplot as plt

from rates_data_processing import compute_moving_average_for_rates_data

start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 10, 1)
currency = "BTCEUR"

data = get_and_manage_rates_data(currency, start_date, end_date)
print("Nombre de cours d'echanges BTC en EURO :", len(data))

m100 = compute_moving_average_for_rates_data(data, 100)
m20 = compute_moving_average_for_rates_data(data, 20)

ma_intervals = [10, 50]
ma_lists = []

for v in ma_intervals:
    ma = compute_moving_average_for_rates_data(data, v)
    ma_lists.append((ma, v))

# # Afficher graph
rates_dates = [datetime.strptime(d["date"], "%Y/%m/%d") for d in data]
rates_values = [r["value"] for r in data]
plt.ylabel(currency)
plt.plot(rates_dates, rates_values)


for ma_items in ma_lists:
    ma_values = [r["value"] for r in ma_items[0]]
    plt.plot(rates_dates, ma_values, label=f"M{ma_items[1]}")

plt.legend()
plt.show()
