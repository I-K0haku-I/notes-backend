# Generated by Django 2.2 on 2019-09-17 14:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0007_auto_20190802_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]
