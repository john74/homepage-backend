# Generated by Django 4.2.3 on 2023-11-02 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0008_alter_setting_bookmark_category_group_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='metric_units',
            field=models.CharField(choices=[('metric', 'Metric'), ('imperial', 'Imperial'), ('standard', 'standard')], default='metric', help_text='<strong>Metric:</strong>\nTemperature Symbol: °C\nTemperature Unit: Celsius\nSpeed: m/s\nHumidity: %\nPressure: hPa\nVisibility: m\n\n<strong>Imperial:</strong>\nTemperature Symbol: °F\nTemperature Unit: Fahrenheit\nSpeed: mph\nHumidity: %\nPressure: hPa\nVisibility: m\n\n<strong>Standard:</strong>\nTemperature Symbol: K\nTemperature Unit: Kelvin\nSpeed: m/s\nHumidity: %\nPressure: hPa\nVisibility: m', max_length=10, verbose_name='System of measurement'),
        ),
    ]