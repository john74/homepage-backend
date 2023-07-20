from django.urls import path

from . import views


app_name = 'bookmarks'

#bookmark category paths
urlpatterns = [
    path('categories/', views.BookmarkCategoryListAPIView.as_view(), name="list_categories"),
    path('bulk-create-categories/', views.BookmarkCategoryBulkCreateAPIView.as_view(), name="bulk_create_categories"),
    path('bulk-delete-categories/', views.BookmarkCategoryBulkDeleteAPIView.as_view(), name="bulk_delete_categories"),
    path('bulk-update-categories/', views.BookmarkCategoryBulkUpdateAPIView.as_view(), name="bulk_update_categories"),
]