# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-07 22:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobslist', '0004_job_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='description',
            field=models.TextField(null=True),
        ),
    ]