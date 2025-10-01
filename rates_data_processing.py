    


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