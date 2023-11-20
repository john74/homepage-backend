import uuid
from django.conf import settings
from django.db import models


class BookmarkSubCategory(models.Model):
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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="User",
    )
    name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="Subcategory",
        verbose_name="Name",
        help_text="50 characters max."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date created"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name='Created by',
        related_name='+',
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date updated"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name='Updated by',
        related_name='+',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Subcategories'

    def __str__(self):
        return f'{self.category.name} {self.name}'

    def save(self, *args, **kwargs):
        # Set the user before saving
        if not self.user_id:
            self.user = self.category.user if self.category else None
        super().save(*args, **kwargs)