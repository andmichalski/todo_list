# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-13 05:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='text',
            field=models.TextField(max_length=1000),
        ),
    ]