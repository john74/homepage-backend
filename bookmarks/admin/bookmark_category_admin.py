from django.contrib import admin


class BookmarkCategoryAdmin(admin.ModelAdmin):
    fields = [
        'id', 'name', 'color',
    ]
    readonly_fields = [
        'id', 'created_at', 'updated_at'
    ]
    list_display = [
        'id', 'name', 'color', 'created_at', 'updated_at'
    ]