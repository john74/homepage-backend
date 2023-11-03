import inspect, uuid

from django.db import models


class Setting(models.Model):
    UNIT_CHOICES = [
        ("metric", "Metric"),
        ("imperial", "Imperial"),
        ("standard", "Standard"),
    ]
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
    system_of_measurement = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default="metric",
        verbose_name="System of measurement",
        help_text=(
            "<strong>Metric:</strong>\n"
            "Temperature Symbol: °C\n"
            "Temperature Unit: Celsius\n"
            "Speed: m/s\n"
            "Humidity: %\n"
            "Pressure: hPa\n"
            "Visibility: m\n\n"
            "\n\n"
            "<strong>Imperial:</strong>\n"
            "Temperature Symbol: °F\n"
            "Temperature Unit: Fahrenheit\n"
            "Speed: mph\n"
            "Humidity: %\n"
            "Pressure: hPa\n"
            "Visibility: m\n\n"
            "\n\n"
            "<strong>Standard:</strong>\n"
            "Temperature Symbol: K\n"
            "Temperature Unit: Kelvin\n"
            "Speed: m/s\n"
            "Humidity: %\n"
            "Pressure: hPa\n"
            "Visibility: m"
        )
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