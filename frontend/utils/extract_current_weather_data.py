import datetime


def extract_current_weather_data(data):
    current_data = data["list"][0]
    city_data = data["city"]

    date = datetime.datetime.utcfromtimestamp(current_data["dt"])
    return {
        "week_day": date.strftime('%A'),
        "month_day": date.strftime('%d'),
        "month": date.strftime('%B'),
        "year": date.strftime('%Y'),
        "hours": date.strftime('%H'),
        "minutes": date.strftime('%M'),
        "city_name": city_data["name"],
        "country_code": city_data["country"],
        "lat": city_data["coord"]["lat"],
        "lon": city_data["coord"]["lon"],
        "temp": current_data["main"]["temp"],
        "description": current_data["weather"][0]["description"]
    }