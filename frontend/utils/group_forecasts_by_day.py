import datetime


def group_forecasts_by_day(data):
    forecasts = {}
    for item in data:
        timestamp = item["dt"]
        date = datetime.datetime.utcfromtimestamp(timestamp)
        day = date.strftime("%Y-%m-%d")

        if day in forecasts:
            forecasts[day].append(item)
        else:
            forecasts[day] = [item]

    return forecasts