# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 08:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='bbox_img_path',
            new_name='bbox_path',
        ),
    ]
