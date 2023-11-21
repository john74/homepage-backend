from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/search-engines/', include('search_engines.urls', namespace='search_engines')),
    path('api/settings/', include('settings.urls', namespace='settings')),
    path('api/users/', include('users.urls', namespace='users')),
    path('api/frontend/', include('frontend.urls', namespace='frontend')),
]

urlpatterns += [
    path('api/bookmarks/', include('bookmarks.urls.bookmarks', namespace='bookmarks')),
    path('api/categories/', include('bookmarks.urls.categories', namespace='categories')),
    path('api/shortcuts/', include('bookmarks.urls.shortcuts', namespace='shortcuts')),
]