# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-04 21:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0039_castingpost_charactertype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='castingpost',
            old_name='paidAmount',
            new_name='paidDescription',
        ),
    ]
