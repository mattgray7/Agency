# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-29 23:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0080_auto_20170929_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilemediapicture',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
