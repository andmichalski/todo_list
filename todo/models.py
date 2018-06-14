# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.


class Task(models.Model):
    STATUS_CHOICES = [("todo", "todo"), ("in_progress", "in_progress"), ("done", "done"), ("to_delete", "to_delete")]

    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, blank=True)

    def __str__(self):
        return self.title

    def update_status(object):
        if object.status == "todo":
            object.status = "in_progress"
        elif object.status == "in_progress":
            object.status = "done"
        else:
            object.status = "to_delete"
        return object
