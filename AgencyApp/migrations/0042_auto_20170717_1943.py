# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-17 19:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0041_postadmin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='castingpost',
            name='hoursPerWeek',
            field=models.TextField(blank=True, default='TBD', max_length=50, null=True),
        ),
    ]