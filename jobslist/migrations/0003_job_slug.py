# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-07 20:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobslist', '0002_auto_20160607_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]
