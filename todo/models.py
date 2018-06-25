# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Task(models.Model):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    TO_DELETE = "to_delete"

    STATUS_CHOICES = ((TODO, "Todo"), (IN_PROGRESS, "In progress"), (DONE, "Done"), (TO_DELETE, "To delete"))

    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
