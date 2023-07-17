from django.contrib.auth.forms import UserChangeForm

from users.models import User


class UserAdminChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)