# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-07 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobslist', '0003_job_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
