# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-01 21:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0020_auto_20170601_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='actorDescriptionEnabled',
            field=models.BooleanField(default=False),
        ),
    ]