import httpx
from rest_framework import status
from rest_framework.response import Response


def get_location_info(setting):
    latitude = getattr(setting, "latitude")
    longitude = getattr(setting, "longitude")
    units = getattr(setting, "system_of_measurement")
    appid = getattr(setting, "open_weather_api_key")

    if not (latitude and longitude and units and appid):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    url = f"{base_url}?lat={latitude}&lon={longitude}&units={units}&appid={appid}"
    return httpx.get(url)
