import uuid

from django.conf import settings
from django.db import models


class Bookmark(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False
    )
    category = models.ForeignKey(
        "bookmarks.BookmarkCategory",
        on_delete=models.CASCADE,
        verbose_name="Bookmark Category",
    )
    sub_category = models.ForeignKey(
        "bookmarks.BookmarkSubCategory",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Bookmark Sub Category",
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
        default="Bookmark",
        verbose_name="Name",
        help_text="50 characters max."
    )
    url = models.URLField(
        max_length=1000,
        verbose_name="Bookmark URL",
        help_text="1000 characters max."
    )
    icon_url = models.URLField(
        max_length=1000,
        verbose_name="Icon URL",
        help_text="1000 characters max."
    )
    is_shortcut = models.BooleanField(
        default=False,
        verbose_name="Is shortcut",
        help_text="The bookmark will be displayed in the shortcuts sidebar."
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
        verbose_name_plural = 'Bookmarks'

    def __str__(self):
        return f'{self.category.name} {self.name}'