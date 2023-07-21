from django.contrib import admin

from .setting_admin import SettingAdmin
from settings.models import Setting


admin.site.register(Setting, SettingAdmin)