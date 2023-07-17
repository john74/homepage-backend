from datetime import datetime

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.forms import UserAdminCreationForm, UserAdminChangeForm
from users.models import User


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    model = User

    fieldsets = [
        (None,
        {
            "fields": [
                "id", "email", "password", "username", "image", "is_superuser",
                "created_at", "created_by", "updated_at", "updated_by",
                "last_login"
            ]
        }
        ),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email", "password1", "password2", "username", "image",
                    "is_superuser",
                ],
            },
        ),
    ]

    readonly_fields = [
        'id', 'created_at', 'created_by',
        'updated_at', 'updated_by', 'last_login'
    ]

    list_display = [
        'id', 'email', 'username', 'is_active',
        'created_at', 'updated_at'
    ]

    list_filter = []

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        if obj.created_by:
            obj.updated_by = request.user
            obj.updated_at = datetime.now()
        else:
            obj.created_by = request.user
        obj.save()