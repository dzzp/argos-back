# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 13:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_testvideo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='frame',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='video',
            name='running_time',
            field=models.FloatField(default=0.0),
        ),
    ]
