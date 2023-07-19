from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/bookmarks/', include('bookmarks.urls', namespace='bookmarks')),
    path('api/users/', include('users.urls', namespace='users')),
]