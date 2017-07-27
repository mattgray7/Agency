# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-27 18:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0046_auto_20170726_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectpost',
            name='length',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='projectpost',
            name='location',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectpost',
            name='projectType',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectpost',
            name='shortDescription',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectpost',
            name='union',
            field=models.BooleanField(default=False),
        ),
    ]