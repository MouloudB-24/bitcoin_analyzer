
def compute_moving_average_for_rates_data(rates, nb_days_interval):
    averages = []
    sum = 0
    divisor = 0

    for i in range(len(rates)):
        sum += rates[i]["value"]
        if i < nb_days_interval:  
            divisor += 1
        else:
            divisor = nb_days_interval
            sum += - rates[i-nb_days_interval]["value"]
        averages.append({"date": rates[i]["date"], "value": sum / divisor})
    return averages


def compute_buy_and_sell_points_from_ma(short_ma, long_ma, threshold_percent=0):
    buy = True
    points = []
    for i in range(len(short_ma)):
        date_str = short_ma[i]["date"]
        sma_value = short_ma[i]["value"]
        lma_value = long_ma[i]["value"]
        muti = 1 + threshold_percent/100
        if buy:
            if sma_value > lma_value*muti:
                points.append((date_str, buy))
                buy = False
        else:
            if sma_value < lma_value/muti:
                points.append((date_str, buy))
                buy = True
    return points


def get_rate_value_for_date_str(date, rates):
    for rate in rates:
        if date == rate["date"]:
            return rate["value"]
    return None


def compute_buy_and_sell_btc(initial_wallet, rates, buy_and_sell_points):
    shares = 0
    current_wallet = initial_wallet
    last_wallet = 0
    
    if buy_and_sell_points[-1][1]:
        buy_and_sell_points = buy_and_sell_points[:-1]
    
    for point in buy_and_sell_points:
        current_date = point[0]
        btc_value = get_rate_value_for_date_str(current_date, rates)
        if btc_value:
            if point[-1]:
                print(f"Le {current_date} j'achete des BTC pour une valeur de {round(current_wallet)} Euros")
                shares = current_wallet / btc_value
                last_wallet = current_wallet
                current_wallet = 0
            else:
                current_wallet = shares * btc_value
                shares = 0
                print(f"Le {current_date} je vends mes BTC. Et je récupère {round(current_wallet)} Euros")
                
                ratio = (current_wallet - last_wallet)/last_wallet*100
                if ratio > 0:
                    print(f"Soit un gain de {round(ratio, 1)}%\n")
                else:
                    print(f"Soit une perte de {round(ratio, 1)}%\n")
        else:
            print("Pas d'achat et/ou du vente de BTC")
    return current_wallet