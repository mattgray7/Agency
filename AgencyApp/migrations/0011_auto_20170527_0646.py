# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-27 06:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0010_castingpost_projectid'),
    ]

    operations = [
        migrations.AddField(
            model_name='actordescriptionstringattribute',
            name='postID',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='actordescriptionstringattribute',
            name='username',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
