import uuid

from django.conf import settings
from django.db import models


class BookmarkCategory(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="User",
    )
    name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="Category",
        verbose_name="Name",
        help_text="The bookmark category name (50 characters max)."
    )
    color = models.CharField(
        max_length=9,
        blank=True,
        null=True,
        default="#000",
        verbose_name="Color",
        help_text="The hex color value should be a maximum of 9 characters, including the # symbol."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date created"
    )
    updated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date updated"
    )
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = [
            "name"
        ]

    def __str__(self):
        return self.name