# Generated by Django 3.1.6 on 2021-03-14 11:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0011_emailheaders_co2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailheaders',
            name='co2',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]