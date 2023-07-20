from django.urls import path

from . import views


app_name = 'bookmarks'

#bookmark category paths
urlpatterns = [
    path('', views.BookmarkCategoryListAPIView.as_view(), name="list"),
    path('create/', views.BookmarkCategoryBulkCreateAPIView.as_view(), name="create"),
    path('delete/', views.BookmarkCategoryBulkDeleteAPIView.as_view(), name="delete"),
    path('update/', views.BookmarkCategoryBulkUpdateAPIView.as_view(), name="update"),
]