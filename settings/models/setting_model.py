import uuid

from django.db import models


class Setting(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False
    )
    latitude = models.CharField(
        max_length=10,
        verbose_name="Latitude",
        help_text="Latitude value in decimal degrees e.g. 39.362483"
    )
    longitude = models.CharField(
        max_length=10,
        verbose_name="Longitude",
        help_text="Longitude value in decimal degrees e.g. 22.940186"
    )
    open_weather_api_key = models.CharField(
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

    class Meta:
        verbose_name_plural = 'Settings'

    def __str__(self):
        return 'Settings'

    def save(self, *args, **kwargs):
        setting = Setting.objects.first()
        country = getattr(setting, 'country', None)

        if country:
            return
        super().save(*args, **kwargs)