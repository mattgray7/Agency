# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-18 21:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0067_auto_20170918_2102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectpost',
            old_name='compensationType',
            new_name='compensation',
        ),
        migrations.RemoveField(
            model_name='projectpost',
            name='compensationDescription',
        ),
    ]
