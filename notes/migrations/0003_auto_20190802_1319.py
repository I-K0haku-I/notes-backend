# Generated by Django 2.2 on 2019-08-02 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_auto_20190528_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='detail',
            field=models.TextField(blank=True),
        ),
    ]