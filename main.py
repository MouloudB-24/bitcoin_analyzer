from datetime import datetime
from rates_data_manage import get_and_manage_rates_data
import matplotlib.pyplot as plt

from rates_data_processing import compute_buy_and_sell_btc, compute_buy_and_sell_points_from_ma, compute_moving_average_for_rates_data

start_date = datetime(2024, 10, 1)
end_date = datetime(2025, 10, 3)
currency = "BTCEUR"

initial_wallet = 1000

data = get_and_manage_rates_data(currency, start_date, end_date)
print("Nb rates :", len(data))

m100 = compute_moving_average_for_rates_data(data, 100)
m20 = compute_moving_average_for_rates_data(data, 20)

ma_values = [10, 50]
ma_lists = []

for value in ma_values:
    ma_list = compute_moving_average_for_rates_data(data, value)
    ma_lists.append((ma_list, value))

buy_and_sell_points = compute_buy_and_sell_points_from_ma(ma_lists[0][0],ma_lists[1][0], 1)

final_wallet = compute_buy_and_sell_btc(initial_wallet, data, buy_and_sell_points)

print(f"\nPériode achat et vente du BTC : {buy_and_sell_points[0][0]} -  {buy_and_sell_points[-1][0]}")
print("Compte initial :", initial_wallet, "Euros")
print("Compte final :", round(final_wallet), "Euros")

# Afficher graph
rates_dates = [datetime.strptime(d["date"], "%Y/%m/%d") for d in data]
rates_values = [r["value"] for r in data]
plt.ylabel(currency)
plt.plot(rates_dates, rates_values)


for ma_items in ma_lists:
    ma_values = [r["value"] for r in ma_items[0]]
    plt.plot(rates_dates, ma_values, label=f"M{ma_items[1]}")

for point in buy_and_sell_points:
    date_obj = datetime.strptime(point[0], "%Y/%m/%d")
    plt.axvline(x=date_obj, color="r" if point[1] else "y")

plt.legend()
plt.show()
