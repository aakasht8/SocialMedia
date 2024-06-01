# Generated by Django 4.2.13 on 2024-05-30 20:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_friendrequest_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendrequest',
            name='status',
            field=models.CharField(default='PENDING', max_length=100),
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 30, 20, 49, 22, 490297)),
        ),
    ]