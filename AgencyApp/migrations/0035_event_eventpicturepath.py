# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 15:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0034_auto_20170425_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='eventPicturePath',
            field=models.CharField(blank=True, default=None, max_length=5000, null=True),
        ),
    ]
