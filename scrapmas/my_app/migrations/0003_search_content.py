# Generated by Django 2.2.4 on 2019-10-31 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_auto_20190808_0328'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='content',
            field=models.TextField(default='No Content'),
        ),
    ]
