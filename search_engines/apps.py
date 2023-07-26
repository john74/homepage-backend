from django.apps import AppConfig


class SearchEnginesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search_engines'

    def ready(self):
        from search_engines.signals import search_engine_signals
