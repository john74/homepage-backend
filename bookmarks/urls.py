from django.urls import path

from . import views


app_name = 'bookmarks'

#bookmark category paths
urlpatterns = [
    path('categories/', views.BookmarkCategoryListAPIView.as_view(), name="list_categories"),
    path('categories/<str:category_id>/', views.BookmarkCategoryDetailAPIView.as_view(), name="category_detail"),
    path('bulk-create-categories/', views.BookmarkCategoryBulkCreateAPIView.as_view(), name="bulk_create_categories"),
    path('bulk-delete-categories/', views.BookmarkCategoryBulkDeleteAPIView.as_view(), name="bulk_delete_categories"),
    path('bulk-update-categories/', views.BookmarkCategoryBulkUpdateAPIView.as_view(), name="bulk_update_categories"),
]

#bookmark paths
urlpatterns += [
    path('', views.BookmarkListAPIView.as_view(), name="list_bookmarks"),
    path('<int:bookmark_id>/', views.BookmarkDetailAPIView.as_view(), name="bookmark_detail"),
    path('bulk-create/', views.BookmarkBulkCreateAPIView.as_view(), name="bulk_create"),
    path('bulk-delete/', views.BookmarkBulkDeleteAPIView.as_view(), name="bulk_delete"),
    path('bulk-update/', views.BookmarkBulkUpdateAPIView.as_view(), name="bulk_update"),
]

#shortcut paths
urlpatterns += [
    path('shortcuts/', views.ShortcutListAPIView.as_view(), name="list_shortcuts"),
    path('bulk-delete-shortcuts/', views.ShortcutBulkDeleteAPIView.as_view(), name="bulk_delete_shortcuts"),
]