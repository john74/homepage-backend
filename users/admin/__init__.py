from django.contrib import admin

from users.models import User
from .user_admin import UserAdmin

admin.site.register(User, UserAdmin)