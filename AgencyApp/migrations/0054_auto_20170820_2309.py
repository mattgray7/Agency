# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-20 23:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0053_auto_20170820_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='castingpost',
            name='compensationType',
            field=models.CharField(blank=True, default='Unpaid', max_length=200, null=True),
        ),
    ]
