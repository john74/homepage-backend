from django.urls import path

from bookmarks import views


app_name = "categories"

urlpatterns = [
    path("", views.BookmarkCategoryListAPIView.as_view(), name="list"),
    path("<str:category_id>/", views.BookmarkCategoryDetailAPIView.as_view(), name="detail"),
    path("bulk-create/", views.BookmarkCategoryBulkCreateAPIView.as_view(), name="bulk_create"),
    path("bulk-delete/", views.BookmarkCategoryBulkDeleteAPIView.as_view(), name="bulk_delete"),
    path("bulk-update/", views.BookmarkCategoryBulkUpdateAPIView.as_view(), name="bulk_update"),
]