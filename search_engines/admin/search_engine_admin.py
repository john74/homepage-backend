from django.contrib import admin


class SearchEngineAdmin(admin.ModelAdmin):
    fields = [
        'id', 'name', 'url', 'method',
        'name_attribute',
    ]
    readonly_fields = [
        'id',
    ]
    list_display = [
        'name', 'url', 'method', 'name_attribute',
    ]