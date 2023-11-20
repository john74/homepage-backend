from django.utils import timezone

import httpx

from base.utils import decrypt_data
from frontend.utils import (
    extract_current_weather_data, extract_extra_weather_data,
    extract_hourly_forecasts, extract_weekly_forecasts,
    group_forecasts_by_day, group_daily_forecasts
)
from frontend.constants import OPEN_WEATHER_UNITS
from settings.models import Setting


def retrieve_weather_data(setting=None, user_id=None):
    setting = Setting.objects.filter(user=user_id).first() if user_id else setting
    if not setting:
        return {}

    latitude = setting.latitude
    longitude = setting.longitude
    units = setting.system_of_measurement
    api_key = decrypt_data(setting.open_weather_api_key)

    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    url = f"{base_url}?lat={latitude}&lon={longitude}&units={units}&lang=en&appid={api_key}"
    response = httpx.get(url)

    if response.status_code != 200:
        return {}

    weather_data =  response.json()
    forecast_type = setting.forecast_type
    current_weather_data = extract_current_weather_data(weather_data)
    extra_info = extract_extra_weather_data(weather_data)
    hourly_forecasts = extract_hourly_forecasts(weather_data)
    weekly_forecasts = extract_weekly_forecasts(weather_data)
    daily_forecasts = group_forecasts_by_day(weekly_forecasts)
    grouped_daily_forecasts = group_daily_forecasts(daily_forecasts)
    units = OPEN_WEATHER_UNITS[setting.system_of_measurement]

    setting.weather_data_last_updated = timezone.now()
    setting.save()

    return {
        "last_updated": setting.weather_data_last_updated,
        "update_interval": setting.weather_data_update_interval,
        "forecast_type": forecast_type,
        "units": units,
        "current": current_weather_data,
        "extra_info": extra_info,
        "forecasts": {
            "hourly": hourly_forecasts,
            "weekly": grouped_daily_forecasts
        }
    }
