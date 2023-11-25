from django.contrib import admin


class BookmarkAdmin(admin.ModelAdmin):
    fields = [
        'id', 'category', 'sub_category', 'user', 'name', 'url', 'icon_url',
        'is_shortcut',
    ]
    readonly_fields = [
        'id', 'user',
    ]
    list_display = [
        'id', 'name', 'category', 'sub_category', 'is_shortcut',
    ]