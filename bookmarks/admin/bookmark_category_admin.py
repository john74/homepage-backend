from django.contrib import admin


class BookmarkCategoryAdmin(admin.ModelAdmin):
    fields = [
        'id', 'name', 'color', 'user',
    ]
    readonly_fields = [
        'id', 'user', 'created_at', 'updated_at'
    ]
    list_display = [
        'id', 'name', 'color', 'created_at', 'updated_at'
    ]