# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-13 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0005_auto_20170513_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpost',
            name='date',
            field=models.DateField(blank=True, default='', null=True),
        ),
    ]