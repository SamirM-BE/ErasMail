# Generated by Django 3.1.6 on 2021-02-21 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailheaders',
            name='received_at',
            field=models.DateTimeField(null=True),
        ),
    ]
