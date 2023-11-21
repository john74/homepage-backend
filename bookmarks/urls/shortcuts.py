from django.urls import path

from bookmarks import views


app_name = "shortcuts"

urlpatterns = [
    path("", views.ShortcutListAPIView.as_view(), name="list"),
    path("bulk-delete/", views.ShortcutBulkDeleteAPIView.as_view(), name="bulk_delete"),
]