import uuid
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom Manager class for the custom User model
    """

    def create_user(self, email, password):
        """
        Create and return a User with an email and password.
        """
        if not email:
            raise TypeError('Users must have an email')

        if not password:
            raise TypeError('Users must have a password')

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Create and return a User with admin permissions.
        """
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    username = models.CharField(
        max_length=50,
        unique=False,
        null=True,
        blank=True
    )
    email = models.EmailField(
        max_length=150,
        unique=True
    )
    image = models.URLField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name="Profile image URL",
        help_text=""
    )
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
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
        blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name='Updated by',
        related_name='+',
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email