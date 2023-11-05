import httpx
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from settings.models import Setting
from frontend.utils import (
    extract_current_weather_data, extract_extra_weather_data,
    extract_hourly_forecasts, extract_weekly_forecasts,
    group_forecasts_by_day, group_daily_forecasts
)
from frontend.constants import OPEN_WEATHER_UNITS

class WeatherAPIView(APIView):

    def get(self, request, *args, **kwargs):
        setting = Setting.objects.first()
        latitude = setting.latitude
        longitude = setting.longitude
        units = setting.system_of_measurement
        api_key = setting.open_weather_api_key

        open_weather_url = f'https://api.openweathermap.org/data/2.5/forecast?' \
                        f'lat={latitude}&lon={longitude}&units={units}' \
                        f'&lang=en&appid={api_key}'
        open_weather_response = httpx.get(open_weather_url)
        weatherData =  open_weather_response.json()

        forecast_type = setting.forecast_type
        current_weather_data = extract_current_weather_data(weatherData)
        extra_info = extract_extra_weather_data(weatherData)
        hourly_forecasts = extract_hourly_forecasts(weatherData)
        weekly_forecasts = extract_weekly_forecasts(weatherData)
        daily_forecasts = group_forecasts_by_day(weekly_forecasts)
        grouped_daily_forecasts = group_daily_forecasts(daily_forecasts)

        units = OPEN_WEATHER_UNITS[setting.system_of_measurement]

        response_data = {
            "forecast_type": forecast_type,
            "units": units,
            "current": current_weather_data,
            "extra_info": extra_info,
            "forecasts": {
                "hourly": hourly_forecasts,
                "weekly": grouped_daily_forecasts
            },
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
