from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from search_engines.constants import SEARCH_ENGINES_DATA
from search_engines.models import SearchEngine
from users.models import User


@receiver(post_save, sender=User)
def add_search_engines(sender=None, **kwargs):
    """
    Populates the Search Engines table with all available engines in
    SEARCH_ENGINES_DATA list, setting Google as the default.
    """
    if SearchEngine.objects.exists():
        return

    for engine_data in SEARCH_ENGINES_DATA:
        if engine_data['name'].lower() == 'google':
            engine_data['is_default'] = True

        SearchEngine.objects.create(**engine_data)

@receiver([post_save, post_delete], sender=SearchEngine)
def set_default_search_engine_on_change(sender, **kwargs):
    """
    Ensures the presence of at least one search engine and enforces a single default engine.
    """
    search_engines = SearchEngine.objects.all()
    # Check if there are no existing SearchEngine objects in the database.
    # If none exist, re-add all the default search engines.
    if not search_engines:
        add_search_engines()
        return

    default_search_engines = search_engines.filter(is_default=True)
    # Ensure there is only one default engine; keep the most recently set default.
    if len(default_search_engines) > 1:
        last_modified_engine = default_search_engines.latest('updated_at')
        rest_default_engines = default_search_engines.exclude(id=last_modified_engine.id)
        rest_default_engines.update(is_default=False)

    if default_search_engines:
        return

    # Set the Google engine as the default if no default engine currently exists.
    google = search_engines.filter(name__icontains='google').first()
    if google:
        google.is_default = True
        google.save()
        return

    # Set the first available engine as default if none currently exist and Google is not an option.
    first_search_engine = search_engines.first()
    first_search_engine.is_default = True
    first_search_engine.save()