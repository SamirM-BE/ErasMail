# Generated by Django 3.1.6 on 2021-03-19 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0021_auto_20210316_1708'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailstats',
            old_name='emails_deleted_count',
            new_name='deleted_emails_count',
        ),
    ]
