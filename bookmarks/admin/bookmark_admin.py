from django.contrib import admin


class BookmarkAdmin(admin.ModelAdmin):
    fields = [
        'id', 'category', 'name', 'url', 'icon_url',
        'is_shortcut',
    ]
    readonly_fields = [
        'id',
    ]
    list_display = [
        'id', 'name', 'category', 'is_shortcut'
    ]