from django.contrib import admin
from django.urls import path, include

# system
urlpatterns = [
    path('admin/', admin.site.urls),
]

# bookmarks app
urlpatterns += [
    path('api/categories/', include('bookmarks.urls.categories', namespace='categories')),
    path('api/sub-categories/', include('bookmarks.urls.sub_categories', namespace='sub_categories')),
    path('api/bookmarks/', include('bookmarks.urls.bookmarks', namespace='bookmarks')),
    path('api/shortcuts/', include('bookmarks.urls.shortcuts', namespace='shortcuts')),
]

# frontend app
urlpatterns += [
    path('api/frontend/', include('frontend.urls.frontend', namespace='frontend')),
]

# search engines app
urlpatterns += [
    path('api/search-engines/', include('search_engines.urls.search_engines', namespace='search_engines')),
]

# settings app
urlpatterns += [
    path('api/settings/', include('settings.urls.settings', namespace='settings')),
]

# users app
urlpatterns += [
    path('api/users/', include('users.urls.users', namespace='users')),
]