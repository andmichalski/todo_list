# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Task(models.Model):
    STATUS_CHOICES = [("todo", "todo"), ("in progress", "in progress"), ("done", "done"), ("to delete", "to delete")]

    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES)
