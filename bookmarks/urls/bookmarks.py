from django.urls import path

from bookmarks import views


app_name = "bookmarks"

urlpatterns = [
    path("", views.BookmarkListAPIView.as_view(), name="list"),
    path("<str:bookmark_id>/", views.BookmarkDetailAPIView.as_view(), name="detail"),
    path("bulk-create/", views.BookmarkBulkCreateAPIView.as_view(), name="bulk_create"),
    path("bulk-delete/", views.BookmarkBulkDeleteAPIView.as_view(), name="bulk_delete"),
    path("bulk-update/", views.BookmarkBulkUpdateAPIView.as_view(), name="bulk_update"),
]