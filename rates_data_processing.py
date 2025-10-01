    


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
        
        
        