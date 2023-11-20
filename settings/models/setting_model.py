import inspect, uuid

from django.conf import settings
from django.db import models
from django.core.validators import (
    MinValueValidator, MaxValueValidator,
)


class Setting(models.Model):
    SYSTEMS_OF_MEASUREMENT = [
        ("metric", "Metric"),
        ("imperial", "Imperial"),
        ("standard", "Standard"),
    ]

    FORECAST_TYPES = [
        ("hourly", "Hourly"),
        ("weekly", "Weekly"),
    ]

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
        choices=SYSTEMS_OF_MEASUREMENT,
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
    forecast_type = models.CharField(
        max_length=6,
        choices=FORECAST_TYPES,
        default="weekly",
        verbose_name="Forecast type",
        help_text="The default type of weather forecast data to be displayed."
    )
    timezone = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Timezone",
        help_text="Automatically derived from latitude and longitude"
    )
    weather_data_last_updated = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Weather data last updated"
    )
    weather_data_update_interval = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        default=60,
        validators=[
            MinValueValidator(limit_value=10),
            MaxValueValidator(limit_value=1440),
        ],
        verbose_name="Weather data refresh interval (minutes)",
        help_text="The duration (in minutes) that must elapse before the weather data can be manually or automatically updated again."
    )
    show_bookmark_sub_categories = models.BooleanField(
        default=True,
        verbose_name="Show bookmark sub categories",
        help_text="If checked, bookmarks will be organized under subcategories within the category."
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