# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 03:27
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0012_auto_20170327_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='profileImage',
            field=models.ImageField(default=None, storage=django.core.files.storage.FileSystemStorage(location='/media/photos'), upload_to=b''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='profilePicture',
            field=models.FileField(default=None, upload_to=b''),
        ),
    ]
