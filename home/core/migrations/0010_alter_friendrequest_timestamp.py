# Generated by Django 4.2.13 on 2024-05-31 21:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_friendrequest_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
