# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-12 04:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gpa', '0002_auto_20160912_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='semester',
            field=models.CharField(max_length=30),
        ),
    ]
