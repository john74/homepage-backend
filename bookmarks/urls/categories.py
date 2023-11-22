from django.urls import (
    path, re_path,
)

from bookmarks import views


app_name = "categories"

urlpatterns = [
    path("", views.BookmarkCategoryListAPIView.as_view(), name="list"),
    path("bulk-create/", views.BookmarkCategoryBulkCreateAPIView.as_view(), name="bulk_create"),
    path("bulk-delete/", views.BookmarkCategoryBulkDeleteAPIView.as_view(), name="bulk_delete"),
    path("bulk-update/", views.BookmarkCategoryBulkUpdateAPIView.as_view(), name="bulk_update"),
    re_path(r"^(?P<category_id>[a-zA-Z0-9-]+)/$", views.BookmarkCategoryDetailAPIView.as_view(), name="detail"),
]