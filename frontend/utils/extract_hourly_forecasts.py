import datetime


def extract_hourly_forecasts(data):
    weatherDataItems = data["list"]
    current_month_day = datetime.datetime.utcfromtimestamp(weatherDataItems[0]["dt"]).strftime('%d')

    hourly_forecasts = []
    for item in weatherDataItems[1:]:
        item_date = datetime.datetime.utcfromtimestamp(item["dt"])
        item_month_day = item_date.strftime('%d')
        if item_month_day != current_month_day:
            break

        forecast = {
            "hours": item_date.strftime('%H'),
            "minutes": item_date.strftime('%M'),
            "temperature": item["main"]["temp"],
            "description": item["weather"][0]["description"],
            "feels_like_temperature": item["main"]["feels_like"],
            "minimum_temperature": item["main"]["temp_min"],
            "maximum_temperature": item["main"]["temp_max"],
            "humidity_percentage": item["main"]["humidity"],
            "wind_speed": item["wind"]["speed"],
        }

        hourly_forecasts.append(forecast)


    return hourly_forecasts
