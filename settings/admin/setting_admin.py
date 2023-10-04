from django.contrib import admin

from settings.models import Setting

class SettingAdmin(admin.ModelAdmin):
    fields = [
        'latitude', 'longitude', 'open_weather_api_key', 'bookmark_category_group_size',
        'metric_units', 'country', 'city', 'timezone',
    ]
    readonly_fields = [
        'country', 'city', 'timezone',
    ]
    list_display = [
        'country', 'city', 'latitude', 'longitude',
        'metric_units', 'timezone',
    ]

    def has_add_permission(self, request):
        # Disallow adding a new instance if a setting already exists.
        return not Setting.objects.exists()