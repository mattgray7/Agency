# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-10 19:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0064_auto_20170906_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='dateOfBirth',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='education',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='gender',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='location',
            field=models.CharField(default='', max_length=200),
        ),
    ]
