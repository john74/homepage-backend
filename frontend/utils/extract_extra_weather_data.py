import datetime


def extract_extra_weather_data(data):
    current_data = data["list"][0]
    city_data = data["city"]

    sunrise_timestamp = city_data["sunrise"]
    sunset_timestamp = city_data["sunset"]

    return {
        "feels_like_temperature": current_data["main"]["feels_like"],
        "minimum_temperature": current_data["main"]["temp_min"],
        "maximum_temperature": current_data["main"]["temp_max"],
        "humidity_percentage": current_data["main"]["humidity"],
        "wind_speed": current_data["wind"]["speed"],
        "sunrise_time": {
            "hour": datetime.datetime.utcfromtimestamp(sunrise_timestamp).strftime('%H'),
            "minutes": datetime.datetime.utcfromtimestamp(sunrise_timestamp).strftime('%M')
        },
        "sunset_time": {
            "hour": datetime.datetime.utcfromtimestamp(sunset_timestamp).strftime('%H'),
            "minutes": datetime.datetime.utcfromtimestamp(sunset_timestamp).strftime('%M')
        }
    }
