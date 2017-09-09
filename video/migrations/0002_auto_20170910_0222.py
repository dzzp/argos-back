# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-09 17:22
from __future__ import unicode_literals

from django.db import migrations, models
import video.validators


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(upload_to='assets/', validators=[video.validators.validate_file_extension]),
        ),
    ]
