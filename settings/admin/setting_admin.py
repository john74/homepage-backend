from django.contrib import admin

from settings.models import Setting

class SettingAdmin(admin.ModelAdmin):
    fields = [
        'latitude', 'longitude', 'open_weather_api_key', "weather_data_update_interval", "weather_data_last_updated", 'bookmark_category_group_size',
        'system_of_measurement', 'forecast_type', 'show_bookmark_sub_categories', 'country', 'city', 'timezone',
    ]
    readonly_fields = [
        'country', 'city', 'timezone', "weather_data_last_updated",
    ]
    list_display = [
        'country', 'city', 'latitude', 'longitude',
        'system_of_measurement', 'timezone',
    ]

    def has_add_permission(self, request):
        # Disallow adding a new instance if a setting already exists.
        return not Setting.objects.exists()