import datetime

from frontend.constants import OPEN_WEATHER_UNITS


def extract_extra_weather_data(data, setting):
    current_data = data["list"][0]
    city_data = data["city"]

    sunrise_timestamp = city_data["sunrise"]
    sunset_timestamp = city_data["sunset"]
    units = OPEN_WEATHER_UNITS[setting.system_of_measurement]

    return [
        {"label": "feels_like", "value": current_data["main"]["feels_like"], "unit": units["temperature"]},
        {"label": "min_temp", "value": current_data["main"]["temp_min"], "unit": units["temperature"]},
        {"label": "max_temp", "value": current_data["main"]["temp_max"], "unit": units["temperature"]},
        {"label": "humidity", "value": current_data["main"]["humidity"], "unit": units["humidity"]},
        {"label": "wind", "value": current_data["wind"]["speed"], "unit": units["wind"]},
        {"label": "sunrise", "value": f"{datetime.datetime.utcfromtimestamp(sunrise_timestamp).strftime('%H')}:{datetime.datetime.utcfromtimestamp(sunrise_timestamp).strftime('%M')}", "unit": ""},
        {"label": "sunset", "value": f"{datetime.datetime.utcfromtimestamp(sunset_timestamp).strftime('%H')}:{datetime.datetime.utcfromtimestamp(sunset_timestamp).strftime('%M')}", "unit": ""},
    ]
