# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-29 05:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0058_postparticipant_privateparticipation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postparticipant',
            old_name='privateParticipation',
            new_name='publicParticipation',
        ),
    ]
