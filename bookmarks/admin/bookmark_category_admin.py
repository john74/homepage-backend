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

    def save_model(self, request, category, form, change):
        # Assign the currently logged-in user to the category's user field
        category.user = request.user
        super().save_model(request, category, form, change)