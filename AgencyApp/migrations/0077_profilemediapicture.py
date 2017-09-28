# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-27 23:52
from __future__ import unicode_literals

import AgencyApp.python.models
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0076_unregisteredproject'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileMediaPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pictureID', models.CharField(max_length=10)),
                ('username', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, default=None, max_length=500, null=True)),
                ('postPicture', models.ImageField(blank=True, default=None, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/media//', location='/Users/MattGray/Projects/Agency/Agency/media/'), upload_to=AgencyApp.python.models.image_directory_path)),
            ],
        ),
    ]