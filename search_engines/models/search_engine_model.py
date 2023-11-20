import inspect, uuid
from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models import (
    Case, When, Value, CharField, Q
)


class SearchEngineManager(models.Manager):

    def create(self, **kwargs):
        name = kwargs.get('name', '')
        url = kwargs.get('url', '')
        lookup = Q(name__iexact=name) | Q(url__iexact=url)

        if self.filter(lookup):
            return

        is_default = kwargs.get('is_default', False)
        if is_default:
            SearchEngine.objects.filter(is_default=True).update(is_default=False)
        return super().create(**kwargs)

class SearchEngine(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="User",
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Name",
        help_text="Search engine name e.g. Google"
    )
    url = models.URLField(
        max_length=1000,
        verbose_name="Action URL",
        help_text="The url of the search engine plus the value of the action attribute of the form e.g. https://www.google.com<b>/search</b>"
    )
    method = models.CharField(
        max_length=50,
        verbose_name="Form method",
        help_text="The value of the form method e.g. GET"
    )
    name_attribute = models.CharField(
        max_length=50,
        verbose_name="Name attribute",
        help_text="The value of the name attribute of the type=search element e.g. q"
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name="Is Default",
        help_text="This search engine will be used as the default. Only one search engine can be set as the default"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        # Update the modification date if the object already exists.
        if not self._state.adding:
            self.updated_at = datetime.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Search Engines'
        ordering = [
            Case(
                When(name__icontains='Google', then=Value('A')),
                default=Value('B'),
                output_field=CharField(),
            ),
            'name',
        ]

    objects = SearchEngineManager()

    def __str__(self):
        return self.name