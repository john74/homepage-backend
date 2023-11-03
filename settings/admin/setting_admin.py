from django.contrib import admin

from settings.models import Setting

class SettingAdmin(admin.ModelAdmin):
    fields = [
        'latitude', 'longitude', 'open_weather_api_key', 'bookmark_category_group_size',
        'system_of_measurement', 'country', 'city', 'timezone',
    ]
    readonly_fields = [
        'country', 'city', 'timezone',
    ]
    list_display = [
        'country', 'city', 'latitude', 'longitude',
        'system_of_measurement', 'timezone',
    ]

    def has_add_permission(self, request):
        # Disallow adding a new instance if a setting already exists.
        return not Setting.objects.exists()