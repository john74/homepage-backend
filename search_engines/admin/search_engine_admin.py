from django.contrib import admin


class SearchEngineAdmin(admin.ModelAdmin):
    fields = [
        'id', 'user', 'name', 'url', 'method',
        'name_attribute', 'is_default',
        'created_at', 'updated_at',
    ]
    readonly_fields = [
        'id', 'user', 'created_at', 'updated_at',
    ]
    list_display = [
        'name', 'url', 'method', 'name_attribute', 'is_default',
    ]