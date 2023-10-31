import datetime


def extract_weekly_forecasts(data):
    weatherDataItems = data["list"]
    current_date = datetime.datetime.utcfromtimestamp(weatherDataItems[0]["dt"])
    current_month_day = current_date.strftime('%d')
    current_month = current_date.strftime('%B')

    forecasts = []
    for item in weatherDataItems:
        item_date = datetime.datetime.utcfromtimestamp(item["dt"])
        month_day = item_date.strftime('%d')
        month = item_date.strftime('%B')

        hours = item_date.strftime('%H')
        if hours not in ["09", "15", "18", "21"]:
            continue

        if (month_day > current_month_day) or (month != current_month):
            forecasts.append(item)

    return forecasts
