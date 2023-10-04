import inspect, uuid

from django.db import models


class Setting(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False
    )
    latitude = models.CharField(
        blank=True,
        null=True,
        max_length=10,
        verbose_name="Latitude",
        help_text="Latitude value in decimal degrees e.g. 39.362483"
    )
    longitude = models.CharField(
        blank=True,
        null=True,
        max_length=10,
        verbose_name="Longitude",
        help_text="Longitude value in decimal degrees e.g. 22.940186"
    )
    open_weather_api_key = models.CharField(
        blank=True,
        null=True,
        max_length=500,
        verbose_name="Open weather API key"
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Country",
        help_text="Automatically derived from latitude and longitude"
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="City",
        help_text="Automatically derived from latitude and longitude"
    )
    metric_units = models.BooleanField(
        default=True,
        verbose_name="Metric units",
        help_text="If set to false, imperial units will be used"
    )
    timezone = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Timezone",
        help_text="Automatically derived from latitude and longitude"
    )
    bookmark_category_group_size = models.PositiveIntegerField(
        default=6,
        blank=True,
        null=True,
        verbose_name="Bookmark categories group size",
        help_text="The number of categories to group together in the UI. "
                  "For example, if you set this to 6 and there are 12 categories, "
                  "they will be displayed as 2 groups of 6 categories each. "
                  "Set to zero or leave this field blank if you don't want any grouping."
    )

    class Meta:
        verbose_name_plural = 'Settings'

    def __str__(self):
        return 'Settings'

    def save(self, *args, **kwargs):
        setting = Setting.objects.first()
        country = getattr(setting, 'country', None)
        caller_function_name = inspect.currentframe().f_back.f_code.co_name.lower()

        # Prevent recursion errors by avoiding additional calls to the save method
        # from the populate_setting_fields signal and other methods.
        # Only allow the update method to call save.
        if country and caller_function_name != 'update':
            return
        super(Setting, self).save(*args, **kwargs)