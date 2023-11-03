from rest_framework import serializers

from settings.models import Setting
from settings.utils import get_location_info


class SettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Setting
        fields = [
            'latitude',
            'longitude',
            'country',
            'city',
            'system_of_measurement',
            'forecast_type',
            'open_weather_api_key',
            'timezone'
        ]