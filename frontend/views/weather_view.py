import httpx
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from frontend.utils import (
    extract_current_weather_data, extract_extra_weather_data,
    extract_hourly_forecasts, extract_weekly_forecasts,
    group_forecasts_by_day, group_daily_forecasts
)


class WeatherAPIView(APIView):

    def get(self, request, *args, **kwargs):
        open_weather_url = f'https://api.openweathermap.org/data/2.5/forecast?lat=52.401621&lon=4.932811&units=metric&lang=en&appid=491f8f7afd8e01c68b5459a12db5a7a5'
        open_weather_response = httpx.get(open_weather_url)
        weatherData =  open_weather_response.json()

        current_weather_data = extract_current_weather_data(weatherData)
        extra_info = extract_extra_weather_data(weatherData)
        hourly_forecasts = extract_hourly_forecasts(weatherData)
        weekly_forecasts = extract_weekly_forecasts(weatherData)
        daily_forecasts = group_forecasts_by_day(weekly_forecasts)
        grouped_daily_forecasts = group_daily_forecasts(daily_forecasts)

        response_data = {
            "current": current_weather_data,
            "extra_info": extra_info,
            "forecasts": {
                "hourly": hourly_forecasts,
                "weekly": grouped_daily_forecasts
            }
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
