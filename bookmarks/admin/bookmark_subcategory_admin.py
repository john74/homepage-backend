from django.contrib import admin


class BookmarkSubCategoryAdmin(admin.ModelAdmin):
    fields = [
        'id', 'category', 'name', 'user', 'created_at',
        'created_by', 'updated_at', 'updated_by'
    ]
    readonly_fields = [
        'id', 'user', 'created_at',
        'created_by', 'updated_at', 'updated_by'
    ]
    list_display = [
        'id', 'name', 'category',
    ]