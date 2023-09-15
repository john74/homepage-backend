from django.contrib import admin


class SearchEngineAdmin(admin.ModelAdmin):
    fields = [
        'id', 'name', 'url', 'method',
        'name_attribute', 'is_default',
        'updated_at',
    ]
    readonly_fields = [
        'id', 'updated_at',
    ]
    list_display = [
        'name', 'url', 'method', 'name_attribute', 'is_default',
    ]