import httpx

def get_location_info(setting):
    latitude = setting.latitude
    longitude = setting.longitude
    units = 'metric' if setting.metric_units else 'imperial'
    appid = setting.open_weather_api_key

    url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units={units}&appid={appid}'
    return httpx.get(url)
