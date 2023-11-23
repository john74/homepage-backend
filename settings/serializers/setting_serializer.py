from rest_framework import serializers

from settings.models import Setting


class SettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Setting
        fields = [
            'latitude',
            'longitude',
            'country',
            'city',
            'system_of_measurement',
            "bookmark_category_group_size",
            "weather_data_last_updated",
            "weather_data_update_interval",
            'forecast_type',
            'open_weather_api_key',
            'timezone',
            'user',
            'show_bookmark_sub_categories',
        ]