from django.db.models.signals import pre_save
from django.dispatch import receiver

from base.utils import encrypt_data
from settings.models import Setting
from settings.utils import get_location_info


@receiver(pre_save, sender=Setting)
def populate_setting_fields(sender, **kwargs):
    setting = kwargs["instance"]
    if setting.country:
        return

    response = get_location_info(setting)
    open_weather_api_key = getattr(setting, "open_weather_api_key")
    setting.open_weather_api_key = encrypt_data(open_weather_api_key)
    if response.status_code != 200:
        return

    location_info = response.json()

    try:
        setting.country = location_info['sys']['country']
        setting.city = location_info['name']
        setting.timezone = location_info['timezone']
    except KeyError:
        return