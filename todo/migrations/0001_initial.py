# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-13 05:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('status', models.CharField(choices=[('todo', 'todo'), ('in progress', 'in progress'), ('done', 'done'), ('to delete', 'to delete')], max_length=11)),
            ],
        ),
    ]
