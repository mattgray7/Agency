# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-16 23:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0050_auto_20170816_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpost',
            name='endTime',
            field=models.TimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='eventpost',
            name='startTime',
            field=models.TimeField(blank=True, default=None, null=True),
        ),
    ]