import datetime


def extract_extra_weather_data(data):
    current_data = data["list"][0]
    city_data = data["city"]

    sunrise_timestamp = city_data["sunrise"]
    sunset_timestamp = city_data["sunset"]

    return [
        {"label": "feels_like", "value": current_data["main"]["feels_like"]},
        {"label": "min_temp", "value": current_data["main"]["temp_min"]},
        {"label": "max_temp", "value": current_data["main"]["temp_max"]},
        {"label": "humidity", "value": current_data["main"]["humidity"]},
        {"label": "wind", "value": current_data["wind"]["speed"]},
        {"label": "sunrise", "value": f"{datetime.datetime.utcfromtimestamp(sunrise_timestamp).strftime('%H')}:{datetime.datetime.utcfromtimestamp(sunrise_timestamp).strftime('%M')}"},
        {"label": "sunset", "value": f"{datetime.datetime.utcfromtimestamp(sunset_timestamp).strftime('%H')}:{datetime.datetime.utcfromtimestamp(sunset_timestamp).strftime('%M')}"},
    ]
