from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from search_engines.constants import SEARCH_ENGINES_DATA
from search_engines.models import SearchEngine
from users.models import User


@receiver(post_save, sender=User)
def add_search_engines(sender=None, **kwargs):
    if SearchEngine.objects.exists():
        return

    for engine_data in SEARCH_ENGINES_DATA:
        if engine_data['name'].lower() == 'google':
            engine_data['is_default'] = True

        SearchEngine.objects.create(**engine_data)

@receiver([post_save, post_delete], sender=SearchEngine)
def set_default_search_engine_on_change(sender, **kwargs):
    search_engines = SearchEngine.objects.all()
    if not search_engines:
        add_search_engines()
        return

    default_search_engine = search_engines.filter(is_default=True)
    if default_search_engine:
        return

    google = search_engines.filter(name__icontains='google').first()
    if google:
        google.is_default = True
        google.save()
        return

    first_search_engine = search_engines.first()
    first_search_engine.is_default = True
    first_search_engine.save()