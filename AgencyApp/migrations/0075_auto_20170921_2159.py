# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-21 21:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0074_auto_20170921_2015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccount',
            name='reelLink',
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='gender',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]