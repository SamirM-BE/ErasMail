# Generated by Django 3.1.6 on 2021-03-16 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('emails', '0020_auto_20210316_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailstats',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
