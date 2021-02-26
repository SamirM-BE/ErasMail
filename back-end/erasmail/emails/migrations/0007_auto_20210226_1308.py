# Generated by Django 3.1.6 on 2021-02-26 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0006_auto_20210226_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='email_header',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachment', to='emails.emailheaders'),
        ),
        migrations.AlterField(
            model_name='emailheaders',
            name='unsubscribe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='newsletter', to='emails.newsletter'),
        ),
    ]