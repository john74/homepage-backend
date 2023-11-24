from django.urls import (
    path, re_path,
)

from bookmarks import views


app_name = "sub_categories"

urlpatterns = [
    path("", views.BookmarkSubCategoryListAPIView.as_view(), name="list"),
    path("bulk-create/", views.BookmarkSubCategoryBulkCreateAPIView.as_view(), name="bulk_create"),
    path("bulk-delete/", views.BookmarkSubCategoryBulkDeleteAPIView.as_view(), name="bulk_delete"),
    path("bulk-update/", views.BookmarkSubCategoryBulkUpdateAPIView.as_view(), name="bulk_update"),
    re_path(r"^(?P<id>[a-zA-Z0-9-]+)/$", views.BookmarkSubCategoryDetailAPIView.as_view(), name="detail"),
]