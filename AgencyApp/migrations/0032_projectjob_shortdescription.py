# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-21 03:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0031_projectrole_shortcharacterdescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectjob',
            name='shortDescription',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
