# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-01 20:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0061_auto_20170829_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='phoneNumber',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
