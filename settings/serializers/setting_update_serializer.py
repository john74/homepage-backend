from rest_framework import serializers

from settings.models import Setting


class SettingUpdateSerializer(serializers.ModelSerializer):

    latitude = serializers.CharField(
        required=False
    )
    longitude = serializers.CharField(
        required=False
    )
    open_weather_api_key = serializers.CharField(
        required=False
    )

    class Meta:
        model = Setting
        fields = [
            'latitude',
            'longitude',
            'country',
            'city',
            'metric_units',
            'open_weather_api_key',
            'timezone'
        ]