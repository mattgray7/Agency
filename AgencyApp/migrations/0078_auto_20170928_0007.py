# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-28 00:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0077_profilemediapicture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profilemediapicture',
            old_name='postPicture',
            new_name='picture',
        ),
    ]
