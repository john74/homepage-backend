from django.contrib import admin

from search_engines.models import SearchEngine

from .search_engine_admin import SearchEngineAdmin

admin.site.register(SearchEngine, SearchEngineAdmin)