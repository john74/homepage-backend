import datetime


def group_daily_forecasts(data_by_day):
    grouped_forecasts = []

    for forecasts in data_by_day.values():
        earliest_forecast = forecasts[0]
        timestamp = earliest_forecast["dt"]
        date = datetime.datetime.utcfromtimestamp(timestamp)

        daily_forecast = {
            "week_day_short_name": date.strftime("%a"),
            "week_day_full_name": date.strftime("%A"),
            "month_short_name": date.strftime("%b"),
            "month_full_name": date.strftime("%B"),
            "month_day": date.strftime("%d"),
            "month_digit": date.strftime("%m"),
            "earliest": {
                "hours": date.strftime('%H'),
                "minutes": date.strftime('%M'),
                "temperature": earliest_forecast['main']['temp'],
                "description": earliest_forecast['weather'][0]['description'],
                "feels_like_temperature": earliest_forecast['main']['feels_like'],
                "min_temperature": earliest_forecast['main']['temp_min'],
                "max_temperature": earliest_forecast['main']['temp_max'],
                "humidity_percent": earliest_forecast['main']['humidity'],
                "wind_speed": earliest_forecast['wind']['speed'],
            }
        }

        rest_forecasts = []
        for forecast in forecasts[1:]:
            timestamp = forecast["dt"]
            date = datetime.datetime.utcfromtimestamp(timestamp)
            rest_forecasts.append({
                "hours": date.strftime('%H'),
                "minutes": date.strftime('%M'),
                "temperature": forecast['main']['temp'],
                "description": forecast['weather'][0]['description'],
                "feels_like_temperature": forecast['main']['feels_like'],
                "min_temperature": forecast['main']['temp_min'],
                "max_temperature": forecast['main']['temp_max'],
                "humidity_percent": forecast['main']['humidity'],
                "wind_speed": forecast['wind']['speed'],
            })

        if len(rest_forecasts) > 2:
            daily_forecast["rest"] = rest_forecasts
            grouped_forecasts.append(daily_forecast)

    return grouped_forecasts