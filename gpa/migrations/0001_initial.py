# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-12 02:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('index', models.CharField(max_length=7, unique=True)),
                ('realName', models.CharField(max_length=100)),
                ('cookie', models.CharField(max_length=100, unique=True)),
                ('lastTry', models.SmallIntegerField()),
                ('grades', models.TextField()),
                ('gpaPoits', models.TextField()),
            ],
        ),
    ]
