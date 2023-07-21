from django.contrib import admin


class SettingAdmin(admin.ModelAdmin):
    fields = [
        'country', 'city', 'latitude', 'longitude',
        'open_weather_api_key', 'units'
    ]
    readonly_fields = [
        'country', 'city',
    ]
    list_display = [
        'country', 'city', 'latitude', 'longitude',
    ]