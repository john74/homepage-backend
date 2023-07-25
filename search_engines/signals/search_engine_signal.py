from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User
from search_engines.search_engines_data import SEARCH_ENGINES_DATA

from search_engines.models import SearchEngine


@receiver(post_save, sender=User)
def add_search_engines(sender, **kwargs):
    if SearchEngine.objects.exists():
        return

    for engine_data in SEARCH_ENGINES_DATA:
        if engine_data['name'].lower() == 'google':
            engine_data['is_default'] = True

        SearchEngine.objects.create(**engine_data)