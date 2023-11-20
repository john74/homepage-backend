from django.utils import timezone
from datetime import datetime, timedelta

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
        user_id = request.user.id
        setting = Setting.objects.filter(user=user_id).first()
        if not setting:
            return Response(data={"error": "No weather data available"}, status=status.HTTP_400_BAD_REQUEST)

        last_updated_time = setting.weather_data_last_updated
        if last_updated_time:
            current_time = timezone.now()
            time_passed_since_last_update = current_time - last_updated_time
            minutes_passed_since_last_update, seconds_passed_since_last_update = divmod(time_passed_since_last_update.total_seconds(), 60)

            update_interval = setting.weather_data_update_interval
            minutes_until_next_update = int(update_interval - minutes_passed_since_last_update)
            if minutes_until_next_update >= 0:
                seconds_until_next_update = int(60 - seconds_passed_since_last_update)
                time_message = (
                    f"{minutes_until_next_update} minute{'s' if minutes_until_next_update != 1 else ''}"
                ) if minutes_until_next_update else (
                    f"{seconds_until_next_update} second{'s' if seconds_until_next_update != 1 else ''}"
                )
                return Response(data={"error": f"Weather data can be updated again in {time_message}."}, status=status.HTTP_400_BAD_REQUEST)

        weather_data = retrieve_weather_data(setting)
        if not weather_data:
            return Response(data={"error": "No weather data available"}, status=status.HTTP_400_BAD_REQUEST)

        weather_data["message"] = "Weather data updated";
        return Response(data=weather_data, status=status.HTTP_200_OK)
