# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-12 04:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gpa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moduleName', models.CharField(max_length=100)),
                ('moduleCode', models.CharField(max_length=10, unique=True)),
                ('semester', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='student',
            old_name='gpaPoits',
            new_name='performance',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='grades',
            new_name='semGPA',
        ),
    ]
