# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-19 05:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0006_auto_20171018_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_path',
            field=models.TextField(),
        ),
    ]
