# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-08-05 04:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gpa', '0009_auto_20170805_0817'),
    ]

    operations = [
        migrations.RenameField(
            model_name='performance',
            old_name='moduleCode',
            new_name='module',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='semesterId',
            new_name='semester',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='index',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='index',
            new_name='user',
        ),
    ]
