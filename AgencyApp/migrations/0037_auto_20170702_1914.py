# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-02 19:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0036_castingpost_actorname'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProjectJob',
        ),
        migrations.AddField(
            model_name='workpost',
            name='shortDescription',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='workpost',
            name='workerName',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
