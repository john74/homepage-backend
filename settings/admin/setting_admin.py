from django.contrib import admin


class SettingAdmin(admin.ModelAdmin):
    fields = [
        'latitude', 'longitude', 'open_weather_api_key', 'units',
        'country', 'city',
    ]
    readonly_fields = [
        'country', 'city',
    ]
    list_display = [
        'country', 'city', 'latitude', 'longitude',
    ]