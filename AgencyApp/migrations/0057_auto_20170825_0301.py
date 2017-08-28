# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-25 03:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0056_auto_20170824_2145'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postID', models.CharField(max_length=10)),
                ('username', models.CharField(max_length=200)),
                ('label', models.CharField(blank=True, default=None, max_length=200, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='projectpost',
            name='shortDescription',
        ),
    ]