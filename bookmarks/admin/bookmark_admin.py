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

    def save_model(self, request, bookmark, form, change):
        # Assign the currently logged-in user to the bookmark's user field
        bookmark.user = request.user
        super().save_model(request, bookmark, form, change)