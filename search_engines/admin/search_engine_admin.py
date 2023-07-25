from django.contrib import admin


class SearchEngineAdmin(admin.ModelAdmin):
    fields = [
        'id', 'name', 'url', 'method',
        'name_attribute', 'is_default',
    ]
    readonly_fields = [
        'id',
    ]
    list_display = [
        'name', 'url', 'method', 'name_attribute', 'is_default',
    ]