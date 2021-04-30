# Generated by Django 3.1.6 on 2021-04-30 23:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0049_merge_20210428_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailstats',
            name='emailbox_carbon_forecast',
            field=models.FloatField(default=0, help_text='Forecast of the emailbox yearly pollution', validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
