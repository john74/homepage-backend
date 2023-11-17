import httpx
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from base.utils import decrypt_data
from bookmarks.models import Bookmark, BookmarkCategory
from bookmarks.serializers import BookmarkSerializer, BookmarkCategorySerializer, ShortcutSerializer
from bookmarks.utils import group_bookmarks, group_bookmark_categories
from search_engines.models import SearchEngine
from search_engines.serializers import SearchEngineSerializer
from settings.models import Setting
from frontend.utils import (
    extract_current_weather_data, extract_extra_weather_data,
    extract_hourly_forecasts, extract_weekly_forecasts,
    group_forecasts_by_day, group_daily_forecasts
)
from frontend.constants import OPEN_WEATHER_UNITS


class HomeListAPIView(APIView):
    bookmark_serializer_class = BookmarkSerializer
    bookmark_category_serializer_class = BookmarkCategorySerializer
    shortcut_serializer_class = ShortcutSerializer
    search_engine_serializer_class = SearchEngineSerializer

    def get(self, request, *args, **kwargs):
        setting = Setting.objects.first()
        latitude = setting.latitude
        longitude = setting.longitude
        units = setting.system_of_measurement
        api_key = decrypt_data(setting.open_weather_api_key)

        open_weather_url = f'https://api.openweathermap.org/data/2.5/forecast?' \
                        f'lat={latitude}&lon={longitude}&units={units}' \
                        f'&lang=en&appid={api_key}'
        open_weather_response = httpx.get(open_weather_url)

        weatherData = {}
        if (open_weather_response.status_code == 200):
            weatherData =  open_weather_response.json()
            forecast_type = setting.forecast_type
            current_weather_data = extract_current_weather_data(weatherData)
            extra_info = extract_extra_weather_data(weatherData)
            hourly_forecasts = extract_hourly_forecasts(weatherData)
            weekly_forecasts = extract_weekly_forecasts(weatherData)
            daily_forecasts = group_forecasts_by_day(weekly_forecasts)
            grouped_daily_forecasts = group_daily_forecasts(daily_forecasts)
            units = OPEN_WEATHER_UNITS[setting.system_of_measurement]
            weatherData = {
                "forecast_type": forecast_type,
                "units": units,
                "current": current_weather_data,
                "extra_info": extra_info,
                "forecasts": {
                    "hourly": hourly_forecasts,
                    "weekly": grouped_daily_forecasts
                }
            }

        all_bookmarks = Bookmark.objects.all()
        serialized_bookmarks = self.bookmark_serializer_class(all_bookmarks, many=True).data
        grouped_bookmarks = group_bookmarks(serialized_bookmarks)

        all_bookmark_categories = BookmarkCategory.objects.all()
        serialized_categories = self.bookmark_category_serializer_class(all_bookmark_categories, many=True).data
        grouped_categories = group_bookmark_categories(serialized_categories)

        all_shortcuts = all_bookmarks.filter(is_shortcut=True)
        serialized_shortcuts = self.shortcut_serializer_class(all_shortcuts, many=True).data

        all_search_engines = SearchEngine.objects.all()
        default_engine = all_search_engines.get(is_default=True)
        non_default_engines = all_search_engines.filter(is_default=False)

        serialized_default_engine = self.search_engine_serializer_class(default_engine).data
        serialized_non_default_engines = self.search_engine_serializer_class(non_default_engines, many=True).data

        response_data = {
            'bookmarks': grouped_bookmarks,
            'categories': grouped_categories,
            'shortcuts': serialized_shortcuts,
            'search_engines': {
                "default": serialized_default_engine,
                "nonDefault": serialized_non_default_engines,
            },
            "weather": weatherData,
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
