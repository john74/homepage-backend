from django.contrib import admin

from .bookmark_admin import BookmarkAdmin
from .bookmark_category_admin import BookmarkCategoryAdmin
from .bookmark_subcategory_admin import BookmarkSubCategoryAdmin

from bookmarks.models import (
    BookmarkCategory, BookmarkSubCategory,
    Bookmark,
)


admin.site.register(BookmarkCategory, BookmarkCategoryAdmin)
admin.site.register(BookmarkSubCategory, BookmarkSubCategoryAdmin)
admin.site.register(Bookmark, BookmarkAdmin)