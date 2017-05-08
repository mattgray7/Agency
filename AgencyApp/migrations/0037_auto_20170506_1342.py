# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-06 13:42
from __future__ import unicode_literals

import AgencyApp.python.models
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgencyApp', '0036_auto_20170506_1154'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollaborationPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postID', models.CharField(max_length=10)),
                ('profession', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postID', models.CharField(max_length=10)),
                ('poster', models.CharField(max_length=200)),
                ('title', models.CharField(blank=True, default=None, max_length=500, null=True)),
                ('description', models.CharField(blank=True, default=None, max_length=5000, null=True)),
                ('postPicturePath', models.CharField(blank=True, default=None, max_length=5000, null=True)),
                ('postPicture', models.ImageField(blank=True, default=None, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/media//', location='/Users/MattGray/Projects/Agency/Agency/media/'), upload_to=AgencyApp.python.models.image_directory_path)),
            ],
        ),
        migrations.CreateModel(
            name='WorkPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postID', models.CharField(max_length=10)),
                ('projectID', models.CharField(max_length=10)),
                ('profession', models.CharField(max_length=200)),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='JobPost',
        ),
    ]