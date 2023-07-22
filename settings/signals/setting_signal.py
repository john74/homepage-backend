from django.db.models.signals import post_save
from django.dispatch import receiver

from settings.models import Setting
from settings.utils import get_location_info


@receiver(post_save, sender=Setting)
def populate_setting_fields(sender, **kwargs):
    setting = Setting.objects.first()
    location_info = get_location_info(setting)

    setting.country = location_info['sys']['country']
    setting.city = location_info['name']
    setting.timezone = location_info['timezone']
    setting.save()