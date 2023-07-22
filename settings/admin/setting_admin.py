from django.contrib import admin


class SettingAdmin(admin.ModelAdmin):
    fields = [
        'latitude', 'longitude', 'open_weather_api_key', 'metric_units',
        'country', 'city', 'timezone',
    ]
    readonly_fields = [
        'country', 'city', 'timezone',
    ]
    list_display = [
        'country', 'city', 'latitude', 'longitude',
        'metric_units', 'timezone',
    ]