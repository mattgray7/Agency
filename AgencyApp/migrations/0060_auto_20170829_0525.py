# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-29 05:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0059_auto_20170829_0525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postparticipant',
            name='publicParticipation',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
