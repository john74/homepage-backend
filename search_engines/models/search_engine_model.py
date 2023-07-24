import inspect, uuid

from django.db import models


class SearchEngine(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False
    )
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Name",
        help_text="Search engine name e.g. Google"
    )
    url = models.URLField(
        max_length=1000,
        unique=True,
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

    class Meta:
        verbose_name_plural = 'Search Engines'
        unique_together = []

    def __str__(self):
        return self.name