# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-17 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0040_auto_20170704_2130'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postID', models.CharField(max_length=10)),
                ('username', models.CharField(max_length=10)),
            ],
        ),
    ]
