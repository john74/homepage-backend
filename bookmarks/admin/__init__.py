from django.contrib import admin

from .bookmark_admin import BookmarkAdmin
from .bookmark_category_admin import BookmarkCategoryAdmin

from bookmarks.models import Bookmark, BookmarkCategory


admin.site.register(BookmarkCategory, BookmarkCategoryAdmin)
admin.site.register(Bookmark, BookmarkAdmin)