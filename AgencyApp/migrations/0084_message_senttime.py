# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-10 17:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0083_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='sentTime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]