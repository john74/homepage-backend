import httpx

def get_location_info(setting):
    latitude = setting.latitude
    longitude = setting.longitude
    units = setting.system_of_measurement
    appid = setting.open_weather_api_key

    url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units={units}&appid={appid}'
    return httpx.get(url)
