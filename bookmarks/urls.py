from django.urls import path

from . import views


app_name = 'bookmarks'

urlpatterns = [
    path('create/', views.BookmarkCategoryBulkCreateAPIView.as_view(), name="create"),
]