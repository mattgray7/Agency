# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 04:12
from __future__ import unicode_literals

import AgencyApp.python.models
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0017_auto_20170404_0410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='profileImage',
            field=models.ImageField(default=None, storage=django.core.files.storage.FileSystemStorage(base_url='/media//profile/', location='/Users/MattGray/Projects/Agency/Agency/media/profile/'), upload_to=AgencyApp.python.models.image_directory_path),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='profilePicture',
            field=models.FileField(default=None, storage=django.core.files.storage.FileSystemStorage(base_url='/media//profile/', location='/Users/MattGray/Projects/Agency/Agency/media/profile/'), upload_to=AgencyApp.python.models.image_directory_path),
        ),
    ]
