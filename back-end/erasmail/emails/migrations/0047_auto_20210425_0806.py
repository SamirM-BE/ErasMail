# Generated by Django 3.1.6 on 2021-04-25 08:06

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0046_remove_emailheaders_is_received'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailheaders',
            name='receiver_email',
            field=models.EmailField(default=django.db.models.expressions.F('owner__email'), max_length=254),
        ),
    ]
