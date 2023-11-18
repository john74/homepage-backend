from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from base.utils import decrypt_data
from frontend.utils import (
    extract_current_weather_data, extract_extra_weather_data,
    extract_hourly_forecasts, extract_weekly_forecasts,
    group_forecasts_by_day, group_daily_forecasts
)
from frontend.constants import OPEN_WEATHER_UNITS
from frontend.utils import retrieve_weather_data
from settings.models import Setting


class WeatherAPIView(APIView):

    def get(self, request, *args, **kwargs):
        weather_data = retrieve_weather_data()
        if not weather_data:
            return Response(data={"error": "No weather data available"}, status=status.HTTP_500_OK)

        weather_data["message"] = "Weather data updated";
        return Response(data=weather_data, status=status.HTTP_200_OK)
