# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    STATUS_CHOICES = [("todo", "todo"), ("in_progress", "in_progress"), ("done", "done"), ("to_delete", "to_delete")]

    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def update_status(self):
        if self.status == "todo":
            self.status = "in_progress"
        elif self.status == "in_progress":
            self.status = "done"
        else:
            self.status = "to_delete"
        return self
