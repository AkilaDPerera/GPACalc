# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-08-17 02:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gpa', '0013_profile_admin_msg'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_msg_showed',
            field=models.BooleanField(default=True),
        ),
    ]
